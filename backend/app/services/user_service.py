from typing import Optional, Tuple
from app.models.user import UserModel
from app.repositories.user_repository import UserRepository
from app.helpers.validators import RequiredFieldsValidator, UserLoginValidator
from app.services.validation_service import ValidationService
from app.utils.socket import call_userenvd
from werkzeug.security import check_password_hash

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def list_users(self):
        return self.repo.get_all()
    
    def get_by_id(self, id) -> UserModel:
        return self.repo.get_by_id(id)

    def get_user_by_email(self, email) -> UserModel:
        return self.repo.get_by_email(email)
    
    def get_user_by_username(self, username) -> UserModel:
        return self.repo.get_by_username(username)

    def add_user(self, name, email, username, password, role="user"):
        user = UserModel(name=name, email=email, username=username, role=role)
        if self.get_user_by_username(user.username):
            return False, "Username already taken.", None

        if self.get_user_by_email(user.email):
            return False, "Email already registered.", None
        
        user.set_password(password)
        try:            
            # Call daemon to create environment
            result, message = call_userenvd(username)
            if not result:
                return False, message, None

            self.repo.add(user) 
            return True, "User is added", user

        except Exception as e:
            self.repo.rollback()
            return False, f"Failed to add user: {str(e)}", None
        
    def login(self, handle: str, password: str) -> Tuple[bool, str, Optional[UserModel]]:
        validators = [
            UserLoginValidator()
        ]
        validation_service = ValidationService(validators)
        is_valid, message = validation_service.validate({"handle": handle, "password": password})
        if not is_valid:
            return False, message, None

        user = UserModel.query.filter(
            (UserModel.username == handle) | (UserModel.email == handle)
        ).first()

        if not user or not check_password_hash(user.password_hash, password):
            return False, "Handle or password is not correct.", None

        if not user.is_active:
            return False, "User is not active!", None

        return True, "Login successful", user

    def delete_user(self, user):
        if user:
            self.repo.delete(user)
            return True
        return False

    def update_user(self, user, **kwargs):
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.repo.update()
        return user