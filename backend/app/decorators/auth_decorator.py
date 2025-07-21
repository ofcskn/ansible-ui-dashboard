from functools import wraps
from app.models.user import UserModel
from app.schemas.api_response_schema import APIResponseSchema
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import request
from flask import jsonify

def role_required(*roles): 
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = UserModel.query.get(user_id)

            if not user:
                return jsonify(APIResponseSchema(
                    success=False,
                    message="User not found.",
                    code=401
                ).to_dict()), 401

            if user.role not in roles:
                return jsonify(APIResponseSchema(
                    success=False,
                    message=f"Access denied. Required roles: {', '.join(roles)}.",
                    code=403
                ).to_dict()), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
