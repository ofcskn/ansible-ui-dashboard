from app.models.user import UserModel
from .base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(UserModel)

    def get_by_username(self, username):
        return self.model.query.filter_by(username=username).first()

    def get_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

