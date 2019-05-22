from flask import current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from app.custom import admin_required
from app.models import db
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
        image = image = ImageModel.find_by_id(image_id)
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
        image = image = ImageModel.find_by_id(image_id)
        if image is None:
            current_app.logger.info(f"Wrong image[id={image_id}]")
            return {"msg": f"Image[id={image_id}] not found."}, 400
        return {"msg": "Update done"}, 200

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
        image.delete_from_db()
        current_app.logger.info(f"Deleted Image[id={image_id}]")
        return {"msg": f"Image[id={image_id}] has been successfully deleted"}, 200   # noqa


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
        db.session.flush()
        current_app.logger.info(f"Image[id={image_id}] updated with Disease[id={disease_id}]")      # noqa
        return {"msg": f"Disease has been successfully updated for image[id={image_id}]"}, 200    # noqa
