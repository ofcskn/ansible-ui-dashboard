from app.extensions import db
from .base import BaseModel

class PlaybookModel(BaseModel):
    __tablename__ = "playbooks"

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    filepath = db.Column(db.String(200), nullable=False)
