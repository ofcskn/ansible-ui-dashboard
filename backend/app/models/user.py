from app.extensions import db
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class UserModel(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(32), unique=False, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), unique=False, nullable=False) 
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(32), nullable=False, default="user") 

    playbooks = relationship('PlaybookModel', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "role": self.role,
        }
