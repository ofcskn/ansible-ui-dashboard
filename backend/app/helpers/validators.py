import re

from app.models.user import UserModel

class Validator:
    def validate(self, data: dict) -> (bool, str):
        raise NotImplementedError()

class UsernameValidator(Validator):
    def validate(self, data):
        username = data.get("username")
        if not username or not re.match(r'^\w{3,20}$', username):
            return False, "Username must be 3-20 characters and contain only letters, numbers, and underscores."
        return True, ""

class PasswordValidator(Validator):
    def validate(self, data):
        password = data.get("password")
        if not password or not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password):
            return False, "Password must be at least 8 characters long and include uppercase, lowercase letters and numbers."
        return True, ""

class EmailValidator(Validator):
    def validate(self, data):
        email = data.get("email")
        if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return False, "Invalid email address."
        return True, ""

class UserLoginValidator(Validator):
    def validate(self, data):
        handle = data.get("handle")
        password = data.get("password")

        if not handle or not password:
            return False, "Handle and password are required."
        return True, ""
    
class PasswordMatchValidator(Validator):
    def validate(self, data):
        if data.get("password") != data.get("confirmPassword"):
            return False, "Passwords are not matching!"
        return True, ""

class RequiredFieldsValidator(Validator):
    def __init__(self, required_fields):
        self.required_fields = required_fields

    def validate(self, data):
        if not all(data.get(field) for field in self.required_fields):
            return False, "Missing required fields."
        return True, ""