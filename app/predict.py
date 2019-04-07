import os
import pickle

import cv2
import numpy as np
import tensorflow as tf
from keras import backend as kb
from keras.models import load_model
from keras.preprocessing.image import img_to_array

from app.utils import APP_DIR_PATH

tf.logging.set_verbosity(tf.logging.ERROR)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def predict_disease(image_path: str, plant_name: str):
    # load the image
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    file_name = os.path.join(APP_DIR_PATH, "static", "images", image_path)
    
    image = cv2.imread(file_name)
    # output = image.copy()

    # pre-process the image for classification
    image = cv2.resize(image, (96, 96))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # load the trained CNN and the label binarizer
    print("[INFO] loading network...")
    # load the corresponding plant model
    mdl = plant_name + ".model"
    model = load_model(os.path.join(
        ROOT_PATH, "trained_models", plant_name, mdl))
    pkl = plant_name + ".pickle"
    lb = pickle.loads(
        open(os.path.join(ROOT_PATH, "trained_models", plant_name, pkl), "rb").read())  # noqa

    # predict the input image
    print("[INFO] Predicting disease...")
    pred = model.predict(image)[0]
    idx = np.argmax(pred)
    label = lb.classes_[idx]
    accuracy = pred[idx] * 100

    results = {"disease": label, "accuracy": accuracy}
    # print(results)
    kb.clear_session()
    return results
