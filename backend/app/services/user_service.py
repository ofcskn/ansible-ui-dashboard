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
        user.set_password(password)
        return self.repo.add(user)

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
