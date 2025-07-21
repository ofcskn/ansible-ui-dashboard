from app.models.playbook import PlaybookModel
from .base_repository import BaseRepository

class PlaybookRepository(BaseRepository):
    def __init__(self):
        super().__init__(PlaybookModel)

    def get_by_name(self, _name):
        return self.model.query.filter_by(name=_name).first()
    
    def get_by_filepath(self, _filepath):
        return self.model.query.filter_by(name=_filepath).first()

    def filter_by_user_id(self, _user_id: int):
        return self.model.query.filter_by(user_id=_user_id).all()

    def filter_by_name(self, _name: str):
        return self.model.query.filter_by(name=_name).all()

    def filter_by_filepath(self, _filepath: str):
        return self.model.query.filter_by(filepath=_filepath).all()

    def filter_by_email(self, _email: str):
        return self.model.query.filter_by(email=_email).all()

    def filter_by_username(self, _username: str):
        return self.model.query.filter_by(username=_username).all()

    def filter_by_is_active(self, _is_active: bool):
        return self.model.query.filter_by(is_active=_is_active).all()
