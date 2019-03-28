from app.models import db


class DiseaseModel(db.Model):
    __tablename__ = "diseases"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    treatment = db.Column(db.String(100), default=None)
    plant_id = db.Column(db.Integer, db.ForeignKey(
        'plants.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('name', 'plant_id'), )

    def __repr__(self):
        return f"Disease(id: {self.id}, name: {self.name}, treatment: {self.treatment}, plant_id: {self.plant_id})"

    @classmethod
    def find_all(cls):
        return cls.query.all()

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
