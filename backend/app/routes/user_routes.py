from app.schemas.api_response_schema import APIResponseSchema
from app.services.user_service import UserService
from app.models.user import UserModel
from app.decorators.auth_decorator import role_required
from app.helpers.validators import EmailValidator, PasswordMatchValidator, PasswordValidator, RequiredFieldsValidator, UsernameValidator
from app.services.validation_service import ValidationService
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, Blueprint, request

users_bp = Blueprint("users", __name__, url_prefix="/users")
service = UserService()

@users_bp.route("/list", methods=["GET"])
def fetch_all():
    data = service.list_users()
    dicted_data = [item.to_dict() for item in data]
    response = APIResponseSchema(success=True, message="Users are fetched", data=dicted_data, code=200)
    return jsonify(response.to_dict())

@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = UserModel.query.get(user_id)
    return jsonify(user.to_dict()), 200

@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    confirmPassword = data.get("confirmPassword")

    required_fields = ["name", "email", "username", "password", "confirmPassword"]
    validators = [
        RequiredFieldsValidator(required_fields),
        UsernameValidator(),
        PasswordValidator(),
        EmailValidator(),
        PasswordMatchValidator(),
    ]
    validation_service = ValidationService(validators)

    is_valid, message = validation_service.validate(data)
    if not is_valid:
        return APIResponseSchema(success=False, message=message, code=400).to_json()

    try:
        status, message, user = service.add_user(name=name, email=email, username=username, password=password)
        if not status:
            return APIResponseSchema(success=status, message=message, code=400).to_json()
        return APIResponseSchema(success=status, message=message, data=user.to_dict(), code=200).to_json()
    except Exception as e:
        return APIResponseSchema(success=False, message=f"A server error is occured {e}.", code=500).to_json()

@users_bp.route("/add", methods=["POST"])
@role_required("admin")
def add_user():
    data = request.get_json() or {}
    user_data = data.get("user", {})

    name = user_data.get("name")
    email = user_data.get("email")
    username = user_data.get("username")
    password = user_data.get("password")

    required_fields = ["name", "email", "username", "password"]
    if not all(user_data.get(field) for field in required_fields):
        return APIResponseSchema(
            success=False,
            message="Missing required fields.",
            code=400
        ).to_json()

    try:
        status, message, user = service.add_user(name=name, email=email, username=username, password=password)
        if not status:
            return APIResponseSchema(success=status, message=message, code=400).to_json()
        return APIResponseSchema(success=status, message=message, data=user, code=200).to_json()
    except Exception as e:
        return APIResponseSchema(success=False, message=f"A server error is occured {e}.", code=500).to_json()