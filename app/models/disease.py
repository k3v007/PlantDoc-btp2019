from app.models import db


class DiseaseModel(db.Model):
    __tablename__ = "diseases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    display_name = db.Column(db.String(150), default=None, nullable=True)
    scientific_name = db.Column(db.String(200), default=None, nullable=True)
    vector = db.Column(db.String(150), default=None, nullable=True)
    nutshell = db.Column(db.Text(), default=None, nullable=True)
    symptoms = db.Column(db.Text(), default=None, nullable=True)
    trigger = db.Column(db.Text(), default=None, nullable=True)
    biological_control = db.Column(db.Text(), default=None, nullable=True)
    chemical_control = db.Column(db.Text(), default=None, nullable=True)
    preventive_measures = db.Column(db.Text(), default=None, nullable=True)
    disease_img = db.Column(db.String(250), default=None, nullable=True)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        'plants.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('name', 'plant_id'), )

    def __repr__(self):
        return f"Disease({self.id}, {self.name})"

    @classmethod
    def find_all(cls):
        return cls.query.order_by(cls.id.asc()).all()

    @classmethod
    def findAll_by_plant(cls, plant_id: int):
        return cls.query.filter_by(plant_id=plant_id).order_by(
            cls.name.asc()).all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_plant(cls, name: str, plant_id: int):
        return cls.query.filter_by(name=name, plant_id=plant_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
