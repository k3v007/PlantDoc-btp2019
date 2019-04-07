import os
from functools import wraps

from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from PIL import Image
from werkzeug.datastructures import FileStorage

from app.models.user import UserModel

APP_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# set directory path for saving images
IMAGE_DIR_PATH = os.path.join(APP_DIR_PATH, "static", "images")


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


# Helper tools for images

def save_image(image_data: FileStorage, folder):
    # Resize the image before saving
    # Image size close to 640x360 or 640x480
    image = Image.open(image_data)    
    max_size = 640, 480
    image.thumbnail(max_size, Image.ANTIALIAS)

    image_path = os.path.join(IMAGE_DIR_PATH, folder, image_data.filename)
    image.save(image_path)

    return image_path


def delete_image(image_path: str):
    os.remove(os.path.join(IMAGE_DIR_PATH, image_path))
