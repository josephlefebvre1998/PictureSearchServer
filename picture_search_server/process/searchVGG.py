from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
import numpy as np

vgg_model = VGG16(weights='imagenet', include_top=True)

img_path = '20180809_130409.jpg'
image_load = image.load_img(img_path, target_size=(224, 224))


def predict(img):
    numpy_image = image.img_to_array(img)
    image_batch = np.expand_dims(numpy_image, axis=0)
    processed_image = preprocess_input(image_batch.copy())

    predictions = vgg_model.predict(processed_image)
    result = decode_predictions(predictions)
    return result


print(predict(image_load))
