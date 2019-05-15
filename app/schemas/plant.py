from app.schemas import ma
from app.models.plant import PlantModel
from app.schemas.disease import DiseaseSchema


class PlantSchema(ma.ModelSchema):
    diseases = ma.Nested(DiseaseSchema, many=True)

    class Meta:
        model = PlantModel
        ordered = True
        load_only = ("images", "diseases")
        include_fk = True
