from marshmallow import RAISE, Schema, fields

from app.models.disease import DiseaseModel
from app.schemas import ma


class DiseaseSchema(ma.ModelSchema):
    class Meta:
        model = DiseaseModel
        ordered = True
        load_only = ("plant_dis", )
        include_fk = True


class DiseaseListSchema(Schema):
    disease_id_list = fields.List(fields.Integer, required=True)

    class Meta:
        strict = True
        unkown = RAISE
