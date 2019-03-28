from app.schemas import ma
from app.models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
