from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.custom import admin_required
from app.models.disease import DiseaseModel
from app.models.image import ImageModel
from app.models.plant import PlantModel
from app.schemas.plant import PlantSchema

plant_schema = PlantSchema()
plant_list_schema = PlantSchema(many=True)


# for plants
class Plants(Resource):
    # Get all plants
    @classmethod
    @jwt_required
    def get(cls):
        return {"plants": plant_list_schema.dump(PlantModel.find_all())}, 200

    # Register a plant
    @classmethod
    @admin_required
    def post(cls):
        plant_data = plant_schema.load(request.get_json())
        plant = PlantModel.find_by_name(plant_data.name)
        if plant:
            current_app.logger.debug(f"Plant<{plant_data.name}> already registered.")   # noqa
            return {"msg": f"Plant[name={plant.name}] already registered."}, 400        # noqa
        try:
            current_app.logger.info(f"Registered {plant_data}")
            plant_data.save_to_db()
            return {"msg": "Plant has been successfully registered"}, 201
        except Exception as err:
            current_app.logger.error(err)
            return {"msg": "Failed to register the plant"}, 500


# for plant by ID
class PlantsID(Resource):
    # Get plant
    @classmethod
    @jwt_required
    def get(cls, plant_id: int):
        plant = PlantModel.find_by_id(plant_id)
        if plant:
            return plant_schema.dump(plant), 200
        return {"msg": f"Plant[id={plant_id}] not found."}, 404

    # Update plant's info
    @classmethod
    @admin_required
    def put(cls, plant_id: int):
        data = plant_schema.load(request.get_json())
        plant = PlantModel.find_by_id(plant_id)
        if plant:
            plant.name = data.name
            plant.save_to_db()
            current_app.logger.info(f"Updated {plant}")
            return {"msg": "Plant's info has been successfully updated"}, 200
        return {"msg": f"Plant[id={plant_id}] not found."}, 404

    # Delete plant
    @classmethod
    @admin_required
    def delete(cls, plant_id: int):
        plant = PlantModel.find_by_id(plant_id)
        if plant:
            plant.delete_from_db()
            current_app.logger.info(f"Deleted {plant}")
            return {"msg": f"Plant has been successfully deleted."}, 200
        return {"msg": f"Plant[id={plant_id}] not found."}, 404


# Get all images of a plant
class PlantsImages(Resource):
    @classmethod
    @admin_required
    def get(cls, plant_id):
        plant = PlantModel.find_by_id(plant_id)
        if plant is None:
            return {"msg": f"Plant[id={plant_id}] not found."}, 404
        return {"images": plant_list_schema.dump(ImageModel.findAll_by_plant(plant_id))}, 200  # noqa


# Get all disease of a plant
class PlantsDiseases(Resource):
    @classmethod
    @jwt_required
    def get(cls, plant_id):
        plant = PlantModel.find_by_id(plant_id)
        if plant is None:
            return {"msg": f"Plant[id={plant_id}] not found."}, 404
        return {"diseases": plant_list_schema.dump(DiseaseModel.findAll_by_plant(plant_id))}, 200  # noqa
