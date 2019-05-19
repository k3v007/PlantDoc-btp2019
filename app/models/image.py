from datetime import datetime

from app.models import db


class ImageModel(db.Model):
    __tablename__ = "images"
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(100), nullable=False, unique=True)
    upload_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    plant_id = db.Column(db.Integer, db.ForeignKey(
        'plants.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    disease_id = db.Column(db.Integer, db.ForeignKey(
        'diseases.id', ondelete='CASCADE'))

    def __init__(self, image_path, plant_id, user_id):
        self.image_path = image_path
        self.plant_id = plant_id
        self.user_id = user_id

    def __repr__(self):
        return f"Image(id: {self.id}, image_path: {self.image_path})"

    # generate presigned_url during fetching only
    @classmethod
    def find_by_user(cls, user_id: int):
        return cls.query.filter_by(user_id=user_id).all()

    # generate presigned_url during fetching only
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.save(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
