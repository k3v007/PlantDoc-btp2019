from app.schemas import ma
from app.models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        ordered = True
        model = UserModel
        load_only = ("images", "password")
