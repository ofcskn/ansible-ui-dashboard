from app.models.playbook import PlaybookModel
from .base_repository import BaseRepository

class PlaybookRepository(BaseRepository):
    def __init__(self):
        super().__init__(PlaybookModel)

    def get_by_name(self, name):
        return self.model.query.filter_by(name=name).first()
