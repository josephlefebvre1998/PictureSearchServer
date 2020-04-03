# !rm -rf ./In-shop-Clothes-From-Deepfashion/
!git clone https://github.com/aryapei/In-shop-Clothes-From-Deepfashion.git
# !rsync -a ./In-shop-Clothes-From-Deepfashion/Img/MEN/ ./In-shop-Clothes-From-Deepfashion/Img/WOMEN/


import numpy as np
from numpy import linalg as LA

from tensorflow.python.keras.applications.vgg16 import VGG16
from tensorflow.python.keras.preprocessing import image
from tensorflow.python.keras.applications.vgg16 import preprocess_input
from tensorflow.python.keras.layers import Cropping2D

from PIL import Image


class VGGNet:
    def __init__(self):
        self.input_shape = (224, 224, 3)
        self.weight = 'imagenet'
        self.pooling = 'max'
        self.model = VGG16(weights=self.weight, input_shape=(self.input_shape[0], self.input_shape[1], self.input_shape[2]), pooling=self.pooling, include_top=False)
        self.model.predict(np.zeros((1, 224, 224, 3)))

    '''
    Use vgg16 model to extract features
    Output normalized feature vector
    '''
    def extract_feat(self, img_path):
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
            raise FileNotFoundError


import os
import h5py
'''
 Extract features and index the images
'''
'''
 Returns a list of filenames for all jpg images in a directory. 
'''


def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

def get_img_list_all():
    img_list_all = []
    f = open("/content/In-shop-Clothes-From-Deepfashion/Eval/list_eval_partition.txt", "r")
    nb_lines = int(f.readline())
    f.readline()
    for i in range(0,nb_lines):
        txt = f.readline()
        x = txt.split()
        img_list_all.append(x[0])
    f.close()
    return img_list_all

def get_img_list_train():
    img_list_train = []
    f = open("/content/In-shop-Clothes-From-Deepfashion/Eval/list_eval_partition.txt", "r")
    nb_lines = int(f.readline())
    f.readline()
    for i in range(0,nb_lines):
        txt = f.readline()
        x = txt.split()
        if x[2] == "train":
            img_list_train.append(x[0])
    f.close()
    return img_list_train

def get_img_list_test():
    img_list_test = []
    f = open("/content/In-shop-Clothes-From-Deepfashion/Eval/list_eval_partition.txt", "r")
    nb_lines = int(f.readline())
    f.readline()
    for i in range(0,nb_lines):
        txt = f.readline()
        x = txt.split()
        if x[2] == "query":
            img_list_test.append(x[0])
    f.close()
    return img_list_test

def get_bbox_list_all():
    bboxs={}
    f = open("/content/In-shop-Clothes-From-Deepfashion/Anno/list_bbox_inshop.txt", "r")
    nb_lines = int(f.readline())
    f.readline()
    for i in range(0,nb_lines):
        txt = f.readline()
        x = txt.split()
        bboxs[x[0]] = (int(x[3]),int(x[4]),int(x[5]),int(x[6]))
    f.close()
    return bboxs


if __name__ == "__main__":

    db = img_paths = '/content/In-Shop-Clothes-From-Deepfashion/'
    img_list = get_img_list_all()
    bboxs = get_bbox_list_all()
    
    print("--------------------------------------------------")
    print("         feature extraction starts")
    print("--------------------------------------------------")
    
    feats = []
    names = []

    model = VGGNet()
    n=0
    for i, img_path in enumerate(img_list):
      values = bboxs[img_path]
      img_path = img_path.replace("i","I",1)
      try:
        im = Image.open("/content/In-shop-Clothes-From-Deepfashion/"+img_path)

        # Crop Image
        area = im.crop(values)
        area.save("tmp.png", "PNG")

        # norm_feat = model.extract_feat("/content/In-shop-Clothes-From-Deepfashion/"+img_path)
        norm_feat = model.extract_feat("tmp.png")
        img_name = img_path
        print(img_name)
        feats.append(norm_feat)
        names.append(img_name)
      except FileNotFoundError:
        pass
      print("extracting feature from image No. %d , %d images in total" %((i+1), len(img_list)))
      n=n+1

    feats = np.array(feats)
    output = 'featureCNN.h5'
    
    print ("--------------------------------------------------")
    print ("      writing feature extraction results ...")
    print ("--------------------------------------------------")

    names = [name.encode('utf8') for name in names]
    h5f = h5py.File(output, 'w')
    h5f.create_dataset('dataset_feat', data=feats)
    h5f.create_dataset('dataset_name', data=names)
    print("model saved")
    h5f.close()

