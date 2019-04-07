import os
import traceback
from secrets import token_hex

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.models import db
from app.models.disease import DiseaseModel
from app.models.image import ImageModel
from app.models.plant import PlantModel
from app.models.user import UserModel
from app.predict import predict_disease
from app.schemas.image import ImageModelSchema, ImageSchema
from app.utils import admin_required, delete_image, save_image

image_schema = ImageSchema()
img_schema = ImageModelSchema()
img_list_schema = ImageModelSchema(many=True)

# set allowed extensions
ALLOWED_IMAGE_EXT = tuple("bmp gif jpg jpeg png".split())


class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls, plant_name: str):
        image = image_schema.load(request.files)["image"]
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        plant = PlantModel.find_by_name(plant_name)

        user_folder = f"user_{user.user_uuid}"
        ext = os.path.splitext(image.filename)[1]
        image.filename = token_hex(8) + ext     # setting random name

        # Check for allowed image extensions
        if ext[1:] not in ALLOWED_IMAGE_EXT:
            return {"messages": f"Extension {ext} not allowed."}, 400

        # save image
        try:
            image_path = save_image(image, folder=user_folder)
        except:     # noqa
            return {"message": "Not a valid image"}, 400

        try:
            disease_result = predict_disease(image_path, plant_name)
        except:     # noqa
            traceback.print_exc()
            delete_image(image_path)
            return {"message": "ML model processing failed"}, 500

        try:
            print(disease_result)
            disease = DiseaseModel.find_by_plant(
                disease_result["disease"], plant.id)
            # if disease is not registered
            if disease is None:
                return {"message": "failed to save image. Disease not found!"}

            # saving image into database
            image_data = ImageModel(
                image_path=image_path, plant_id=plant.id,
                user_id=user_id, disease_id=disease.id
            )
            db.session.add(image_data)
            db.session.commit()
        except:     # noqa
            traceback.print_exc()
            return {"message": "failed to save image to database"}, 500

        return {"result": disease_result}


class ImageList(Resource):
    @classmethod
    @admin_required
    def get(cls):
        return {"images": img_list_schema.dump(ImageModel.find_all())}, 200
