from flask import current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.custom import admin_required
from app.models.disease import DiseaseModel
from app.models.image import ImageModel
from app.models.user import UserModel
from app.schemas.image import ImageModelSchema

img_schema = ImageModelSchema()
img_list_schema = ImageModelSchema(many=True)


# Get all imagess
class Images(Resource):
    @classmethod
    @admin_required
    def get(cls):
        return {"images": img_list_schema.dump(ImageModel.find_all())}, 200


class ImagesID(Resource):
    # Get image
    @classmethod
    @jwt_required
    def get(cls, image_id: int):
        image = ImageModel.find_by_id(image_id)
        user = UserModel.find_by_id(get_jwt_identity())
        if image is None:
            current_app.logger.info(f"Wrong image[id={image_id}]")
            return {"msg": f"Image[id={image_id}] not found."}, 400
        # image can be accessed by the owner and admin only
        if image.user_id != user.id and user.admin is False:
            current_app.logger.info(
                f"Userd[id={user.id}] tried to access Image[id={image.id}] owned by User[id={image.user_id}]")    # noqa
            return {"msg": "Access denied."}, 403
        return {"images": img_schema.dump(ImageModel.find_by_id(image_id))}, 200     # noqa

    # Update image details
    @classmethod
    @admin_required
    def put(cls, image_id: int):
        image = ImageModel.find_by_id(image_id)
        if image is None:
            current_app.logger.info(f"Wrong image[id={image_id}]")
            return {"msg": f"Image[id={image_id}] not found."}, 400

        img = img_schema.load(request.get_json(),
                              partial=("plant_id", "user_id", "image_path"))
        img.upload_date = image.upload_date if img.upload_date is None else img.upload_date   # noqa
        img.client_img_path = image.client_img_path if img.client_img_path is None else img.client_img_path   # noqa
        image.upload_date = img.upload_date
        image.client_img_path = img.client_img_path
        try:
            image.save_to_db()
            current_app.logger.info(f"Updated {image}")
            return {"msg": f"Image[id={image_id}] info has been successfully updated"}, 201 # noqa
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"msg": "Failed to update the image's info"}, 500

    # Delete image
    @classmethod
    @jwt_required
    def delete(cls, image_id: int):
        image = ImageModel.find_by_id(image_id)
        user = UserModel.find_by_id(get_jwt_identity())

        if image is None:
            current_app.logger.info(f"Wrong image[id={image_id}]")
            return {"msg": f"Image[id={image_id}] not found."}, 400
        # image can be deleted by the owner and admin only
        if image.user_id != user.id and user.admin is False:
            current_app.logger.info(
                f"Userd[id={user.id}] tried to delete Image[id={image.id}] owned by User[id={image.user_id}]")    # noqa
            return {"msg": "Access denied."}, 403
        try:
            image.delete_from_db()
            current_app.logger.info(f"Deleted Image[id={image_id}]")
            return {"msg": f"Image[id={image_id}] has been successfully deleted"}, 200   # noqa
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"msg": "Failed to delete the image"}, 500


# Update image's disease id
class ImagesDiseasesUpdate(Resource):
    @classmethod
    @jwt_required
    def put(cls, image_id: int, disease_id: int):
        image = ImageModel.find_by_id(image_id)
        disease = DiseaseModel.find_by_id(disease_id)
        if image is None:
            current_app.logger.info(f"Wrong image[id={image_id}]")
            return {"msg": f"Image[id={image_id}] not found."}, 400

        if disease is None:
            current_app.logger.info(f"Wrong disease[id={disease_id}]")
            return {"msg": f"Disease[id={disease_id}] not found."}, 400

        image.disease_id = disease_id
        try:
            image.save_to_db()
            current_app.logger.info(f"Image[id={image_id}] updated with Disease[id={disease_id}]")      # noqa
            return {"msg": f"Disease has been successfully updated for image[id={image_id}]"}, 200    # noqa
        except Exception as err:     # noqa
            current_app.logger.error(err)
            return {"msg": "Failed to update the image's info"}, 500