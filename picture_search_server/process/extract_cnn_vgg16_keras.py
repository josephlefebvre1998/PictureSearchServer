
import numpy as np
from numpy import linalg as LA

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input


class VGGNet:
    def __init__(self):
        self.input_shape = (150, 150, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model = VGG16(weights=self.weight, input_shape=(self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling=self.pooling, include_top=False)
        self.model.predict(np.zeros((1, 150, 150, 3)))

    '''
    Use vgg16 model to extract features
    Output normalized feature vector
    '''
    def extract_feat_path(self, img_path):
        try:
            img = image.load_img(img_path, target_size=(self.input_shape[0], self.input_shape[1]))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)
            feat = self.model.predict(img)
            norm_feat = feat[0] / LA.norm(feat[0])
            return norm_feat
        except FileNotFoundError:
            print("file not found : "+img_path)

    def extract_feat_image(self, img):
        try:
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)
            feat = self.model.predict(img)
            norm_feat = feat[0] / LA.norm(feat[0])
            return norm_feat
        except FileNotFoundError:
            print("file not found : ")

