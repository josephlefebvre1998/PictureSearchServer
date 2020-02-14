# !git clone https://github.com/aryapei/In-shop-Clothes-From-Deepfashion.git
# !rsync -a ./In-shop-Clothes-From-Deepfashion/Img/MEN/ ./In-shop-Clothes-From-Deepfashion/Img/WOMEN/


from keras.applications import InceptionResNetV2
from keras.preprocessing.image import ImageDataGenerator
from keras import layers
from keras import models
from keras import optimizers

conv_base = InceptionResNetV2(weights='imagenet', include_top=False, input_shape=(150,150,3))
# conv_base = VGG16(weights='imagenet', include_top=False, input_shape=(299,299,3))

conv_base.summary()

model = models.Sequential()
model.add(conv_base)
model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dropout(0.3))
model.add(layers.Dense(17, activation='sigmoid'))

model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizers.RMSprop(lr=1e-4),metrics=['acc'])

directory = "/content/In-shop-Clothes-From-Deepfashion/Img/WOMEN"

train_datagen = ImageDataGenerator(
  rescale=1./255,
  rotation_range=40,
  width_shift_range=0.2,
  height_shift_range=0.2,
  shear_range=0.2,
  zoom_range=0.2,
  horizontal_flip=True,)

test_datagen = ImageDataGenerator(rescale=1./255)

batch_size = 128

train_generator = train_datagen.flow_from_directory(
  directory,
  target_size=(150, 150),
  batch_size=batch_size,
  class_mode='binary')

print(train_generator.class_indices)

validation_generator = test_datagen.flow_from_directory(
  directory,
  target_size=(150, 150),
  batch_size=batch_size,
  class_mode='binary')

history = model.fit_generator(
  train_generator,
  steps_per_epoch=300,
  epochs=32,
  validation_data= validation_generator,
  validation_steps= batch_size)

model.save('model_keras.h5')