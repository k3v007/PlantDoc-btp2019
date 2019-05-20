
import glob
import os

import numpy as np
import tensorflow as tf
from flask import current_app
from keras import applications
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.preprocessing.image import img_to_array, load_img

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.logging.set_verbosity(tf.logging.ERROR)


def predict_disease(img_path: str, model_path: str):
    # load weights and classes of model
    TOP_MODEL_WEIGHTS = glob.glob(os.path.join(model_path, "*.h5"))[0]
    TOP_MODEL_CLASSES = glob.glob(os.path.join(model_path, "*.npy"))[0]
    class_dictionary = np.load(TOP_MODEL_CLASSES, allow_pickle=True).item()

    current_app.logger.info("Loading and Preprocessing image...")
    try:
        image = load_img(img_path, target_size=(224, 224))
    except Exception as e:
        current_app.logger.error(e.args[1])
    image = img_to_array(image)

    # important! otherwise the predictions will be '0'
    image = image / 255
    image = np.expand_dims(image, axis=0)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    # get the bottleneck prediction from the pre-trained VGG16 model
    bottleneck_prediction = model.predict(image)

    # build top model
    model = Sequential()
    model.add(Flatten(input_shape=bottleneck_prediction.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(units=len(class_dictionary), activation='sigmoid'))
    model.load_weights(TOP_MODEL_WEIGHTS)

    # use bottleneck prediction on top model to get the final classification
    disease_predicted = model.predict_classes(bottleneck_prediction)
    probability = max(model.predict_proba(bottleneck_prediction)[0])
    classMap = {v: k for k, v in class_dictionary.items()}
    disease_name = classMap[disease_predicted[0]]

    # result
    result = {}
    result["Disease"] = disease_name
    result["Probability"] = str(probability)
    current_app.logger.info({"img_path": img_path, "result": result})

    return result