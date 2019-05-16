from flask_restful import Resource
from app.utils import admin_required
from app.schemas.plant import PlantSchema
from app.models.plant import PlantModel
from app.models import db
from flask import request
import traceback


plant_schema = PlantSchema()
plant_list_schema = PlantSchema(many=True)


class Plant(Resource):
    @classmethod
    def get(cls, name: str):
        plant = PlantModel.find_by_name(name)
        if plant:
            return plant_schema.dump(plant), 200
        return {"message": "Plant not found."}, 404

    @classmethod
    @admin_required
    def delete(cls, name: str):
        plant = PlantModel.find_by_name(name)
        if plant:
            plant.delete_from_db()
            return {"message": f"Plant '{name}' successfully deleted."}, 200
        return {"message": "Plant not found."}, 404


class RegisterPlants(Resource):
    @classmethod
    @admin_required
    def post(cls):
        data_json = request.get_json()
        plants = list()
        for plant_json in data_json["plants"]:
            plant_data = plant_schema.load(plant_json)
            plant = PlantModel.find_by_name(plant_data.name)
            # report error if any plant in the request is already registered
            if plant:
                return {"message": f"Plant '{plant.name}' already registered."}, 400
            # add all unregistered plants
            plants.append(plant_data)

        # save the plants to database
        try:
            db.session.add_all(plants)
            db.session.commit()
            return {"message": "All plant(s) registered successfully"}, 201
        except:     # noqa
            traceback.print_exc()
            return {"message": "Failed to register the plant(s)"}, 500


class PlantList(Resource):
    @classmethod
    @admin_required
    def get(cls):
        return {"plants": plant_list_schema.dump(PlantModel.find_all())}, 200
