import os

from PIL import Image
from werkzeug.datastructures import FileStorage


APP_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# set directory path for saving images
IMAGE_DIR_PATH = os.path.join(APP_DIR_PATH, "static", "images")


# ==============================================================================

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

# ==============================================================================