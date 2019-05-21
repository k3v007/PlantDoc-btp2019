from flask import current_app, request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.custom import admin_required
from app.models.image import ImageModel
from app.schemas.image import ImageModelSchema, ImageSchema

image_schema = ImageSchema()
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
    # @classmethod
    # @jwt_required
    # def get(cls):
    #     user_id = get_jwt_identity()
    #     return {"images": img_list_schema.dump(ImageModel.find_by_user(user_id))}, 200

    @classmethod
    @jwt_required
    def put(cls, image_id: int):
        pass
