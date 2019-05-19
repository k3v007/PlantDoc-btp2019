import os
from datetime import datetime

from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.custom import admin_required
from app.models import db
from app.models.disease import DiseaseModel
from app.models.image import ImageModel
from app.models.plant import PlantModel
from app.models.user import UserModel
from app.predict import predict_disease
from app.schemas.image import ImageB64Schema, ImageModelSchema, ImageSchema
from app.utils import APP_DIR_PATH, delete_image, save_image

image_schema = ImageSchema()
img_schema = ImageModelSchema()
img_list_schema = ImageModelSchema(many=True)
img_b64_schema = ImageB64Schema()

# set allowed extensions
ALLOWED_IMAGE_EXT = tuple("bmp gif jpg jpeg png".split())


class ImageUpload(Resource):
    @classmethod
    @jwt_required
    def post(cls, plant_id: int):
        image = image_schema.load(request.files)["image"]
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        plant = PlantModel.find_by_id(plant_id)
        if plant is None:
            return {"message": "Wrong plant id provided."}, 400

        user_folder = user.user_dir
        ext = os.path.splitext(image.filename)[1]
        upload_dt = datetime.now()
        dt_format = f"user{user_id}_%H:%M:%S_%d-%m-%Y"
        image.filename = upload_dt.strftime(dt_format) + ext

        # Check for allowed image extensions
        if ext[1:] not in ALLOWED_IMAGE_EXT:
            return {"messages": f"Extension {ext} not allowed."}, 400

        # save client image on disk
        # file should be of image type only
        try:
            image_path = save_image(image, folder=user_folder)
        except:     # noqa
            return {"message": "Not a valid image"}, 400

        # predict the disease
        try:
            model_path = os.path.join(APP_DIR_PATH,
                                      'disease_prediction_models',
                                      plant.name)
            result = predict_disease(image_path, model_path)
            disease = DiseaseModel.find_by_plant(name=result["Disease"],
                                                 plant_id=plant.id)
            # Check if disease name is properly registerd
            if disease is None:
                current_app.loggger.error(f"Predicted disease <{predicted_disease}> not found!")    # noqa
                delete_image(image_path)
                return {"message": "The server encountered an internal error and was unable to complete your request"}, 500     # noqa

        except Exception as e:     # noqa 
            current_app.logger.error(e.args[0])
            delete_image(image_path)
            return {"message": "The server encountered an internal error and was unable to complete your request"}, 500     # noqa

        # save image into database
        try:
            image_data = ImageModel(
                image_path=image_path, plant_id=plant.id,
                user_id=user_id, disease_id=disease.id,
                upload_date=upload_dt,
            )
            db.session.add(image_data)
            db.session.commit()
        except Exception as e:     # noqa
            current_app.logger.error(e.args[0])
            delete_image(image_path)
            return {"message": "The server encountered an internal error and was unable to complete your request"}, 500     # noqa

        # if all above processes completed successfully, then return result
        return result, 200


# class ImageB64Upload(Resource):
#     @classmethod
#     @jwt_required
#     def post(cls, plant_name: str):
#         json_data = request.get_json()
#         user_id = get_jwt_identity()
#         user = UserModel.find_by_id(user_id)
#         plant = PlantModel.find_by_name(plant_name)
#         image_string = img_b64_schema.load(json_data)["image_b64"]

#         user_folder = user.user_folder

#         # save image
#         try:
#             image_path = save_image(image_string, folder=user_folder)
#         except:     # noqa
#             return {"message": "Not a valid base64 string"}, 400

#         try:
#             # saving image into database
#             image_data = ImageModel(
#                 image_path=image_path, plant_id=plant.id,
#                 user_id=user_id
#             )
#             db.session.add(image_data)
#             db.session.commit()
#         except:     # noqa
#             traceback.print_exc()
#             return {"message": "Failed to save image to database"}, 500

#         # current_app.logger.info(f"image_b64: {image_string['image_b64']}")
#         return {"message": "Image uploaded Successfully."}, 200


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
