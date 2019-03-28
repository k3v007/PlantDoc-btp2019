import os
from flask_restful import Resource
from app.schemas.image import ImageSchema, ImageModelSchema
from app.models.user import UserModel
from app.models.image import ImageModel
from app.models.plant import PlantModel
from app.models.disease import DiseaseModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import save_image, get_basename, get_extension, admin_required
from flask_uploads import UploadNotAllowed
from secrets import token_hex
from flask import request
import traceback
from app.models import db
from app.tf_disease_classifier.classify import classify_disease
from app.utils import APP_DIR_PATH

image_schema = ImageSchema()
img_schema = ImageModelSchema()
img_list_schema = ImageModelSchema(many=True)


class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls, plant_name: str):
        data = image_schema.load(request.files)
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        plant = PlantModel.find_by_name(plant_name)

        folder = f"user_{user.user_uuid}"
        ext = get_extension(data["image"])
        try:
            data["image"].filename = token_hex(16) + ext
            image_path = save_image(data["image"], folder=folder)
            basename = get_basename(image_path)
            # print(image_path)
            try:
                disease_result = classify_disease(image_path, plant_name)
            except:
                traceback.print_exc()
                os.remove(os.path.join(APP_DIR_PATH,
                                       "static", "images", image_path))
                return {"message": "ML model processing failed"}, 500

            try:
                print(disease_result)
                disease = DiseaseModel.find_by_plant(
                    disease_result["disease"], plant.id)
                # if disease is not registered
                if disease is None:
                    return {"message": "failed to save image. Disease not Found!"}

                image_data = ImageModel(
                    image_path=basename, plant_id=plant.id, user_id=user_id, disease_id=disease.id)
                db.session.add(image_data)
                db.session.commit()
            except:
                traceback.print_exc()
                return {"message": "failed to save image to database"}
            return {"result": disease_result}
        except UploadNotAllowed:
            return {"messages": f"Extension {ext} not allowed."}


class ImageList(Resource):
    @classmethod
    @admin_required
    def get(cls):
        return {"images": img_list_schema.dump(ImageModel.find_all())}, 200
