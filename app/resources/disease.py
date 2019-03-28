from flask_restful import Resource
from app.utils import admin_required
from app.schemas.disease import DiseaseSchema
from app.models.disease import DiseaseModel
from app.models.plant import PlantModel
from app.models import db
from flask import request
import traceback


disease_schema = DiseaseSchema()
disease_list_schema = DiseaseSchema(many=True)


class Disease(Resource):
    @classmethod
    @admin_required
    def get(cls, name: str, plant_id: int):
        disease = DiseaseModel.find_by_plant(name, plant_id)
        if disease:
            return disease_schema.dump(disease), 200
        return {"message": "Disease not found."}, 404

    @classmethod
    @admin_required
    def delete(cls, name: str, plant_id: int):
        disease = DiseaseModel.find_by_plant(name, plant_id)
        if disease:
            disease.delete_from_db()
            return {"message": f"Disease '{name}' with Plant <{plant_id}> deleted successfully ."}, 200
        return {"message": "Disease not found."}, 404


class RegisterDiseases(Resource):
    @classmethod
    @admin_required
    def post(cls):
        data_json = request.get_json()
        diseases = list()
        for disease_json in data_json["diseases"]:
            disease_data = disease_schema.load(disease_json)
            # search if plant exists or not
            plant = PlantModel.find_by_name(disease_json["plant_name"])
            if plant is None:
                return {"message": f"Plant <{disease_data.plant_name}> not found!"}, 400

            # plant is found, now check whether disease is already registered or not
            disease = DiseaseModel.query.filter_by(
                name=disease_data.name, plant_id=plant.id).first()

            # report error if any disease in the request is already registered
            # unique(disease name, plant_id)
            if disease:
                return {"message": f"Disease '{disease.name}' already registered with Plant '{plant.name}'."}, 400

            # add all unregistered diseases
            disease_data.plant_id = plant.id    # since plant_id was None
            diseases.append(disease_data)

        # save the diseases to database
        try:
            db.session.add_all(diseases)
            db.session.commit()
            return {"message": "All disease(s) registered successfully"}, 201
        except:
            traceback.print_exc()
            return {"message": "Failed to register the disease(s)"}, 500


class DiseaseList(Resource):
    @classmethod
    @admin_required
    def get(cls):
        return {"diseases": disease_list_schema.dump(DiseaseModel.find_all())}, 200
