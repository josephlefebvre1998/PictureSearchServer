from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.applications.imagenet_utils import decode_predictions
from process.extract_cnn_vgg16_keras import VGGNet
from keras.models import load_model
from keras import models
from keras import layers
import numpy as np
import os
import h5py


def model_load():
    # model = load_model(os.path.normpath(os.path.join(os.getcwd(), "./models/featureDNN.h5")))
    # # model.summary()
    # print("load success")
    # return model
    h5f = h5py.File(os.path.normpath(os.path.join(os.getcwd(), "./models/featureCNN.h5")), 'r')
    feats = h5f['dataset_feat'][:]
    img_names = h5f['dataset_name'][:]
    h5f.close()
    return feats, img_names


def predict(img, max_res=3):
    # init VGGNet16 model
    model = VGGNet()

    # extract query image's feature, compute simlarity score and sort
    queryVec = model.extract_feat_image(img)
    scores = np.dot(queryVec, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]
    # print(rank_score)

    # number of top retrieved images to show
    imlist = [images[index] for i, index in enumerate(rank_ID[0:max_res])]
    return imlist


def predict_test():
    # # CNN retrieval
    img_path = os.path.normpath(os.path.join(os.getcwd(), "./tests_images/20180809_130409.jpg"))

    # init VGGNet16 model
    model = VGGNet()

    # extract query image's feature, compute similarity score and sort
    queryVec = model.extract_feat_path(img_path)
    scores = np.dot(queryVec, feats.T)
    rank_ID = np.argsort(scores)[::-1]
    rank_score = scores[rank_ID]
    # print(rank_score)

    # number of top retrieved images to show
    maxres = 3
    imlist = [images[index] for i, index in enumerate(rank_ID[0:maxres])]

    return imlist


feats, images = model_load()

if __name__ == '__main__':
    predict_test()
