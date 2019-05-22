from app.models.user import UserModel
from app.schemas import ma


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        ordered = True
        load_only = ("images", "password")
        dump_only = ("user_dir", "member_since", "last_seen",)
