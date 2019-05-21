from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.custom import admin_required
from app.models.disease import DiseaseModel
from app.schemas.disease import DiseaseSchema
from app.models.plant import PlantModel

disease_schema = DiseaseSchema()
disease_list_schema = DiseaseSchema(many=True)


# for diseases
class Diseases(Resource):
    # Get all diseases
    @classmethod
    @admin_required
    def get(cls):
        return {"diseases": disease_list_schema.dump(DiseaseModel.find_all())}, 200     # noqa

    @classmethod
    @admin_required
    def post(cls):
        disease_data = disease_schema.load(request.get_json())
        plant = PlantModel.find_by_id(disease_data.plant_id)
        if plant is None:
            return {"message": f"Plant[id={data.disease_id}] not found."}, 400    # noqa

        disease = DiseaseModel.query.filter_by(name=disease_data.name,
                                               plant_id=plant.id).first()
        if disease:
            current_app.logger.debug("<disease, plant> already registered")
            return {"message": f"Disease '{disease_data.name}' already registered with Plant[id={plant.id}]."}, 400  # noqa
        try:
            disease_data.save_to_db()
            current_app.logger.info(f"Registered {disease_data}")
            return {"message": "Disease successfully registered."}, 201
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"message": "Failed to register the disease(s)"}, 500


class DiseasesID(Resource):
    # Get disease
    @classmethod
    @jwt_required
    def get(cls, disease_id: int):
        disease = DiseaseModel.find_by_id(disease_id)
        if disease:
            return disease_schema.dump(disease), 200
        return {"message": f"Disease[id={disease_id}] not found."}, 404

    # Update disease's info
    @classmethod
    @admin_required
    def put(cls, disease_id: int):
        disease_json = request.get_json()
        _disease = disease_schema.load(disease_json,
                                       partial=("name", "plant_name",))
        disease = DiseaseModel.query.get(disease_id)
        if disease is not None:
            disease.scientific_name = _disease.scientific_name
            disease.vector = _disease.vector
            disease.nutshell = _disease.nutshell
            disease.trigger = _disease.trigger
            disease.symptoms = _disease.symptoms
            disease.biological_control = _disease.biological_control
            disease.chemical_control = _disease.chemical_control
            disease.preventive_measures = _disease.preventive_measures
            disease.save_to_db()
            current_app.logger.info(f"Updated {disease}")
            return {"message": f"Disease[id={disease_id}] updated successfully."}, 200
        return {"message": "Disease not found."}, 404

    # Delete disease
    @classmethod
    @admin_required
    def delete(cls, disease_id: int):
        disease = DiseaseModel.find_by_id(disease_id)
        if disease:
            disease.delete_from_db()
            return {"message": f"Disease[id={disease_id}] deleted successfully."}, 200     # noqa
        return {"message": f"Disease[id={disease_id}] not found."}, 404
