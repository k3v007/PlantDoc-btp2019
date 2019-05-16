from app.schemas import ma
from app.models.disease import DiseaseModel
from marshmallow import fields


class DiseaseSchema(ma.ModelSchema):
    plant_name = fields.Str(required=True)

    class Meta:
        model = DiseaseModel
        ordered = True
        load_only = ("plant_dis", )
        dump_only = ("plant_id", )
        include_fk = True
