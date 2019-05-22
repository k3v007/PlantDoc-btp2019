from app.models import db
from app.models.disease import DiseaseModel  # noqa
from app.models.image import ImageModel  # noqa


class PlantModel(db.Model):
    __tablename__ = "plants"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    diseases = db.relationship('DiseaseModel', backref="plant_dis",
                               cascade="all, delete-orphan", lazy=True)
    images = db.relationship('ImageModel', backref="plant_img",
                             cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"Plant({self.id}, {self.name})"

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
