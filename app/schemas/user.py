from app.schemas import ma
from app.models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        ordered = True
        model = UserModel
        ordered = True
        load_only = ("images", "password")
        dump_only = ("user_dir",)
