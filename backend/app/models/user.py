from app.extensions import db
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship

class UserModel(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(32), unique=False, nullable=False)
    _email = db.Column("email", db.String(256), unique=True, nullable=False)
    _username = db.Column("username", db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), unique=False, nullable=False) 
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    role = db.Column(db.String(32), nullable=False, default="user") 

    playbooks = relationship('PlaybookModel', back_populates='user', cascade="all, delete-orphan")

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None:
            self._email = None
        else:
            self._email = value.strip().lower()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if value is None:
            self._username = None
        else:
            self._username = value.strip().lower()

    def set_password(self, password: str):
        combined = self.email + password
        self.password_hash = generate_password_hash(combined)

    def verify_password(self, password: str) -> bool:
        combined = self.email + password
        return check_password_hash(self.password_hash, combined)
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "role": self.role,
        }
