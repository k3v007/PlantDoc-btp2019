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
            current_app.logger.info(f"Wrong plant[id={disease_data.plant_id}]")
            return {"msg": f"Plant[id={data.disease_id}] not found."}, 400    # noqa

        disease = DiseaseModel.query.filter_by(name=disease_data.name,
                                               plant_id=plant.id).first()
        if disease:
            current_app.logger.debug(f"[{disease}, {plant}] already registered")    # noqa
            return {"msg": f"Disease '{disease_data.name}' already registered with Plant[id={plant.id}]."}, 400  # noqa
        try:
            disease_data.save_to_db()
            current_app.logger.info(f"Registered {disease_data}")
            return {"msg": "Disease successfully registered."}, 201
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"msg": "Failed to register the disease(s)"}, 500


class DiseasesID(Resource):
    # Get disease
    @classmethod
    @jwt_required
    def get(cls, disease_id: int):
        disease = DiseaseModel.find_by_id(disease_id)
        if disease:
            return disease_schema.dump(disease), 200
        return {"msg": f"Disease[id={disease_id}] not found."}, 404

    # Update disease's info
    @classmethod
    @admin_required
    def put(cls, disease_id: int):
        disease_json = request.get_json()
        _disease = disease_schema.load(disease_json,
                                       partial=("name", "plant_id",))
        disease = DiseaseModel.query.get(disease_id)
        if disease is not None:
            disease.scientific_name = disease.scientific_name if _disease.scientific_name is None else _disease.scientific_name                     # noqa
            disease.vector = disease.vector if _disease.vector is None else _disease.vector                                                         # noqa
            disease.nutshell = disease.nutshell if _disease.nutshell is None else _disease.nutshell                                                 # noqa
            disease.trigger = disease.trigger if _disease.trigger is None else _disease.trigger                                                     # noqa
            disease.symptoms = disease.symptoms if _disease.symptoms is None else _disease.symptoms                                                 # noqa
            disease.biological_control = disease.biological_control if _disease.biological_control is None else  _disease.biological_control        # noqa
            disease.chemical_control = disease.chemical_control if _disease.chemical_control is None else _disease.chemical_control                 # noqa
            disease.preventive_measures = disease.preventive_measures if _disease.preventive_measures is None else _disease.preventive_measures     # noqa
            try:
                disease.save_to_db()
                current_app.logger.info(f"Updated {disease}")
                return {"msg": f"Disease[id={disease_id}] updated successfully."}, 200  # noqa
            except Exception as err:     # noqa
                current_app.logger.error(err)
                return {"msg": "Failed to update the disease's info"}, 500
        return {"msg": "Disease not found."}, 404

    # Delete disease
    @classmethod
    @admin_required
    def delete(cls, disease_id: int):
        disease = DiseaseModel.find_by_id(disease_id)
        if disease:
            disease.delete_from_db()
            return {"msg": f"Disease[id={disease_id}] deleted successfully."}, 200     # noqa
        return {"msg": f"Disease[id={disease_id}] not found."}, 404
