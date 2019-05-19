import os
from typing import List

from werkzeug.security import check_password_hash

from app.models import db
from app.models.image import ImageModel  # noqa
from app.utils import IMAGE_DIR_PATH


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    user_dir = db.Column(db.String(32), nullable=False, default="user")
    images = db.relationship(
        'ImageModel', backref="user",  cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"User(name: {self.name}, email: {self.email})"    # noqa

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

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

    def create_img_dir(self) -> None:
        self.user_dir = "-".join(["user", str(self.id), self.email])
        os.makedirs(os.path.join(IMAGE_DIR_PATH, self.user_dir))
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
