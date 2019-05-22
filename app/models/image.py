import os
from datetime import datetime

from app.models import db


class ImageModel(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(250), nullable=False, unique=True)
    upload_date = db.Column(db.DateTime(), nullable=False,
                            default=datetime.utcnow)
    client_img_path = db.Column(db.String(250), default=None)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        'plants.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey(
        'diseases.id', ondelete='CASCADE'))

    def __repr__(self):
        return f"Image({self.id}, image_path: {self.image_path})"

    @classmethod
    def findAll_by_user(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def findAll_by_plant(cls, plant_id: int):
        return cls.query.filter_by(plant_id=plant_id).all()

    @classmethod
    def find_by_id(cls, img_id: int):
        return cls.query.get(img_id)

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # delete from disk also
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        db.session.delete(self)
        db.session.commit()
