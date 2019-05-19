import traceback

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.models import db
from app.models.disease import DiseaseModel
from app.models.plant import PlantModel
from app.schemas.disease import DiseaseSchema
from app.custom import admin_required

disease_schema = DiseaseSchema()
disease_list_schema = DiseaseSchema(many=True)


class Disease(Resource):
    @classmethod
    @jwt_required
    def get(cls, disease_id: int):
        disease = DiseaseModel.find_by_id(disease_id)
        if disease:
            return disease_schema.dump(disease), 200
        return {"message": f"Disease[id={disease_id}] not found."}, 404

    @classmethod
    @admin_required
    def delete(cls, disease_id: int):
        disease = DiseaseModel.find_by_id(disease_id)
        if disease:
            disease.delete_from_db()
            return {"message": f"Disease[id={disease_id}] deleted successfully."}, 200     # noqa
        return {"message": f"Disease[id={disease_id}] not found."}, 404


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
                return {"message": f"Plant <{disease_data.plant_name}> not found!"}, 400    # noqa

            # plant is found, now check whether disease is already registered or not    # noqa
            disease = DiseaseModel.query.filter_by(
                name=disease_data.name, plant_id=plant.id).first()

            # report error if any disease in the request is already registered
            # unique(disease name, plant_id)
            if disease:
                return {"message": f"Disease '{disease.name}' already registered with Plant '{plant.name}'."}, 400  # noqa

            # add all unregistered diseases
            disease_data.plant_id = plant.id    # since plant_id was None
            diseases.append(disease_data)

        # save the diseases to database
        try:
            db.session.add_all(diseases)
            db.session.commit()
            return {"message": "All disease(s) registered successfully"}, 201
        except:     # noqa
            traceback.print_exc()
            return {"message": "Failed to register the disease(s)"}, 500


class UpdateDisease(Resource):
    @classmethod
    @admin_required
    def put(cls, disease_id: int):
        disease_json = request.get_json()
        _disease = disease_schema.load(disease_json,
                                       partial=("name", "plant_name",))
        disease = DiseaseModel.query.get(disease_id)

        if disease is not None:
            disease.nutshell = _disease.nutshell
            disease.trigger = _disease.trigger
            disease.symptoms = _disease.symptoms
            disease.biological_control = _disease.biological_control
            disease.chemical_control = _disease.chemical_control
            disease.preventive_measures = _disease.preventive_measures
            disease.save_to_db()
            return {"message": f"Disease[id={disease_id}] updated successfully."}, 200

        return {"message": "Disease not found."}, 404


class DiseaseListOfPlant(Resource):
    @classmethod
    @jwt_required
    def get(cls, plant_id: int):
        plant = PlantModel.query.get(plant_id)
        if plant is not None:
            return {"diseases": disease_list_schema.dump(
                DiseaseModel.find_all_by_plant(plant_id=plant_id))}, 200
        return {"message": "Disease not found."}, 404


class DiseaseList(Resource):
    @classmethod
    @admin_required
    def get(cls):
        return {"diseases": disease_list_schema.dump(DiseaseModel.find_all())}, 200     # noqa
