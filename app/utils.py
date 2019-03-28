import os
import re
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import UserModel
from functools import wraps
from typing import Union
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES

# To suppress Tensorflow warnings
APP_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
IMAGE_SET = UploadSet("images", IMAGES)  # set name and allowed extensions


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(_id=user_id)
        if not user._admin:
            return {"msg": "Admins only"}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


# Helper tools for images
def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    return IMAGE_SET.save(image, folder, name)


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    if isinstance(file, FileStorage):
        return file.filename
    return file


def get_basename(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
