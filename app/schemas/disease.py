from app.schemas import ma
from app.models.disease import DiseaseModel


class DiseaseSchema(ma.ModelSchema):
    class Meta:
        model = DiseaseModel
        ordered = True
        load_only = ("plant_dis", )
        include_fk = True
