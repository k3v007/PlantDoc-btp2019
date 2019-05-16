import logging
import os
import traceback
from secrets import token_hex

from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.aws import upload_image, upload_b64_image
from app.models import db
from app.models.disease import DiseaseModel
from app.models.image import ImageModel
from app.models.plant import PlantModel
from app.models.user import UserModel
from app.predict import predict_disease
from app.schemas.image import ImageModelSchema, ImageSchema, ImageB64Schema
from app.utils import admin_required, delete_image

image_schema = ImageSchema()
img_schema = ImageModelSchema()
img_list_schema = ImageModelSchema(many=True)
img_b64_schema = ImageB64Schema()

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
            image_path = upload_image(image, folder=user_folder)
        except:     # noqa
            return {"message": "Not a valid image"}, 400

        # return {"image_path": image_path}, 200

        # try:
        #     disease_result = predict_disease(image_path, plant_name)
        # except:     # noqa
        #     traceback.print_exc()
        #     delete_image(image_path)
        #     return {"message": "ML model processing failed"}, 500

        try:
            # saving image into database
            image_data = ImageModel(
                image_path=image_path, plant_id=plant.id,
                user_id=user_id
            )
            db.session.add(image_data)
            db.session.commit()
        except:     # noqa
            traceback.print_exc()
            return {"message": "failed to save image to database"}, 500

        # return {"result": disease_result}
        return {"message": "Image uploaded successfully!"}, 200


class ImageB64Upload(Resource):
    @classmethod
    @jwt_required
    def post(cls, plant_name: str):
        json_data = request.get_json()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        plant = PlantModel.find_by_name(plant_name)
        image_string = img_b64_schema.load(json_data)["image_b64"]

        user_folder = f"user_{user.user_uuid}"

        # save image
        try:
            image_path = upload_b64_image(image_string, folder=user_folder)
        except:     # noqa
            return {"message": "Not a valid base64 string"}, 400

        try:
            # saving image into database
            image_data = ImageModel(
                image_path=image_path, plant_id=plant.id,
                user_id=user_id
            )
            db.session.add(image_data)
            db.session.commit()
        except:     # noqa
            traceback.print_exc()
            return {"message": "Failed to save image to database"}, 500

        # current_app.logger.info(f"image_b64: {image_string['image_b64']}")
        return {"message": "Image uploaded Successfully."}, 200


class ImageList(Resource):
    @classmethod
    @admin_required
    def get(cls):
        return {"images": img_list_schema.dump(ImageModel.find_all())}, 200


class ImageListOfUser(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        return {"images": img_list_schema.dump(ImageModel.find_by_user(user_id))}, 200
