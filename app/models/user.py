from app.models import db
from typing import List
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.image import ImageModel


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    _admin = db.Column(db.Boolean, nullable=False, default=False)
    user_uuid = db.Column(db.String(32), nullable=False, default=uuid4().hex)
    images = db.relationship(
        'ImageModel', backref="user",  cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"User(user_uuid: {self.user_uuid}, username: {self.username}, email: {self.email}, admin: {self._admin})"

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
