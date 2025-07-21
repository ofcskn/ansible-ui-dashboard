from app.models.user import UserModel
from app.repositories.user_repository import UserRepository

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
        self.repo.add(user)
        return True, "User is added",user

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
