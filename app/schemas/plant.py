from app.schemas import ma
from app.models.plant import PlantModel


class PlantSchema(ma.ModelSchema):
    class Meta:
        model = PlantModel
        ordered = True
        load_only = ("images", "diseases")
        include_fk = True
