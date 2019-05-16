from marshmallow import Schema, fields
from werkzeug.datastructures import FileStorage

from app.models.image import ImageModel
from app.schemas import ma


class FileStorageField(fields.Field):
    default_error_messages = {
        "invalid": "Not a valid image"
    }

    def _deserialize(self, value, attr, data) -> FileStorage:
        if value is None:
            return None

        if not isinstance(value, FileStorage):
            self.fail("invalid")    # raises ValidationError

        return value


class ImageSchema(Schema):
    image = FileStorageField(required=True)


class ImageModelSchema(ma.ModelSchema):
    class Meta:
        model = ImageModel
        load_only = ("user", "plant_img", "image_path")
        dump_only = ("image_url")
        include_fk = True


class ImageB64Schema(Schema):
    image_b64 = fields.String(required=True)
