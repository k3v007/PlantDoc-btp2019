import os
import re
import shutil
from datetime import datetime
from typing import List

from flask import current_app
from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash

from app.models import db
from app.models.image import ImageModel  # noqa


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    password = db.Column(db.String(100), nullable=False)
    user_dir = db.Column(db.String(100), nullable=False, default="user")
    admin = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    member_since = db.Column(db.DateTime(), nullable=False,
                             default=datetime.now)
    last_seen = db.Column(db.DateTime(), nullable=False,
                          default=datetime.now)
    images = db.relationship('ImageModel', backref="user",
                             cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"User({self.name}, {self.email})"

    @validates('email')
    def validate_email(cls, key, email):
        if email is None:
            raise AssertionError("No email provided.")
        if not re.match('^(\D)+(\w)*((\.(\w)+)?)+@(\D)+(\w)*((\.(\D)+(\w)*)+)?(\.)[a-z]{2,}$', email):  # noqa
            raise AssertionError("Invalid email provided.")
        return email

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_all(cls) -> List["UserModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
        # save user before to get the id
        # create user image directory
        self.user_dir = "-".join(["user", str(self.id), self.email])
        os.makedirs(os.path.join(current_app.config["CLIENTS_DIR_PATH"],
                                 "img", self.user_dir), exist_ok=True)
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        # delete user directory
        DIR = os.path.join(current_app.config["CLIENTS_DIR_PATH"],
                           "img", self.user_dir)
        if os.path.exists(DIR):
            shutil.move(DIR, current_app.config["TEMP_DIR_PATH"])
        db.session.delete(self)
        db.session.commit()

    def ping(self) -> None:
        self.last_seen = datetime.now()
        db.session.add(self)
        db.session.commit()
