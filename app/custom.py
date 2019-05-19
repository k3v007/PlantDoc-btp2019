
from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models.user import UserModel


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(_id=user_id)
        if not user.admin:
            return {"msg": "Admins only"}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper
