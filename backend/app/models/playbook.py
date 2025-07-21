from app.extensions import db
from .base import BaseModel
from sqlalchemy.orm import relationship

class PlaybookModel(BaseModel):
    __tablename__ = "playbooks"

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    filepath = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = relationship('UserModel', back_populates='playbooks')

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "name": self.name,
            "description": self.description,
            "filepath": self.filepath,
            "user_id": self.user_id,
            "user": self.user.to_dict()
        })
        return base