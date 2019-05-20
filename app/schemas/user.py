from marshmallow import RAISE, Schema, fields

from app.models.user import UserModel
from app.schemas import ma


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        ordered = True
        load_only = ("images", "password")
        dump_only = ("user_dir", "active", "member_since", "last_seen",)


class UserUpdateSchema(Schema):
    name = fields.String(required=True)
    active = fields.Boolean(required=True)

    class Meta:
        strict = True
        ordered = True
        unknown = RAISE
