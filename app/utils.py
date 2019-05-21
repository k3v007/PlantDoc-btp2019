import os

from flask import current_app
from PIL import Image
from werkzeug.datastructures import FileStorage

# ==============================================================================

# Helper tools for images


def save_image(image_data: FileStorage, folder):
    # Resize the image before saving
    # Image size close to 640x360 or 640x480
    image = Image.open(image_data)
    max_size = 640, 480
    image.thumbnail(max_size, Image.ANTIALIAS)

    image_path = os.path.join(current_app.config["CLIENTS_DIR_PATH"], "img",
                              folder, image_data.filename)
    image.save(image_path)

    return image_path


def delete_image(image_path: str):
    os.remove(image_path)

# ==============================================================================
