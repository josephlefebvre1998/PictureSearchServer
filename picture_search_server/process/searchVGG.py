from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from keras.models import load_model
from keras import models
from keras import layers
import numpy as np
import os


def model_load():
    model = load_model(os.path.normpath(os.path.join(os.getcwd(), "./models/model_deep_fashion_2.h5")))
    # model.summary()
    print("load success")
    return model


def predict(img):
    numpy_image = image.img_to_array(img)
    image_batch = np.expand_dims(numpy_image, axis=0)
    processed_image = preprocess_input(image_batch.copy())

    predictions = model.predict(processed_image)
    result = decode_predictions(predictions)
    return result


def predict_test():
    img_path = os.path.normpath(os.path.join(os.getcwd(), "./tests_images/20180809_130409.jpg"))
    image_load = image.load_img(img_path, target_size=(150, 150))
    print(predict(image_load))


model = model_load()

if __name__ == '__main__':
    predict_test()
