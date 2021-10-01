import os
from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3

local_weights_file = 'model/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5'

pre_trained_model = InceptionV3(input_shape=(320, 240, 3),
                              include_top=False,
                              weights=None)

pre_trained_model.load_weights(local_weights_file)

for layer in pre_trained_model.layers:
  layer.trainable = False

pre_trained_model.summary()

last_layer = pre_trained_model.get_layer('mixed7')
print('last layer output shape: ', last_layer.output.shape)
last_output = last_layer.output

from tensorflow.keras.optimizers import RMSprop

x = layers.Flatten()(last_output)
x = layers.Dense(1024, activation='relu')(x)
x = layers.Dense(5, activation='sigmoid')(x)
# x = layers.Dense(12, activation='sigmoid')(x)

model = Model(pre_trained_model.input, x)

model.compile(
            optimizer=RMSprop(lr=0.0001),
            # optimizer = 'adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy'])

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define our example directories and files
base_dir = '/content/drive/MyDrive/sensor_img/some_data'

train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'validation')

# Add our data-augmentation parameters to ImageDataGenerator
train_datagen = ImageDataGenerator(rescale=1./255.,
                                 rotation_range=40,
                                 width_shift_range=0.2,
                                 height_shift_range=0.2,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)

# Note that the validation data should not be augmented!
test_datagen = ImageDataGenerator(rescale=1./255.)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(train_dir,
                                                  batch_size=20,
                                                  class_mode='binary',
                                                  target_size=(320, 240))

# Flow validation images in batches of 20 using test_datagen generator
validation_generator = test_datagen.flow_from_directory(validation_dir,
                                                      batch_size=20,
                                                      class_mode='binary',
                                                      target_size=(320, 240))

from tensorflow.keras import models, layers, callbacks

# val_loss 가능, 가장 좋은 값 저장
my_save = callbacks.ModelCheckpoint(
    f'/content/drive/MyDrive/sensor_img/model/inception_v3(binary, sparse_categorical_crossentropy)_checkpoint_model.h5',
    monitor='val_accuracy')

# 학습 정체시 학습률 줄이기
my_rate = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                      patience=20)

hist = model.fit(
  train_generator,
  validation_data=validation_generator,
  callbacks = [my_save, my_rate],
  # steps_per_epoch=100,
  epochs=20,
  batch_size = 256,
  #validation_steps=50,
  verbose=1
)

model.save(f'/content/drive/MyDrive/sensor_img/model/inception_v3(binary, sparse_categorical_crossentropy)_model.h5')

import matplotlib.pyplot as plt

fig, loss_ax = plt.subplots()

acc_ax = loss_ax.twinx()

loss_ax.plot(hist.history['loss'], 'y', label='train loss')
loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')

acc_ax.plot(hist.history['accuracy'], 'b', label='train acc')
acc_ax.plot(hist.history['val_accuracy'], 'g', label='val acc')

loss_ax.set_xlabel('epoch')
loss_ax.set_ylabel('loss')
acc_ax.set_ylabel('accuray')

loss_ax.legend(loc='upper left')
acc_ax.legend(loc='lower left')

plt.show()

import os
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing import image
import tensorflow as tf

class_names = sorted(os.listdir('/content/drive/MyDrive/sensor_img/some_data/train'))
# class_names = sorted(os.listdir('/content/drive/MyDrive/sensor_image/all data/train'))
print(class_names)

image_folder = '/content/drive/MyDrive/sensor_img/test/some_data'
images = os.listdir(image_folder)


def predict_img(img_name):
    path = (f'{image_folder}/{img_name}')
    img = image.load_img(path, target_size=(320, 240))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    classes = model.predict(x)
    recognized_result = format(class_names[np.argmax(classes)])

    print(f'{img_name[:-4]} is {recognized_result}')


def predict_img1(img_name):
    path = (f'{image_folder}/{img_name}')
    img = image.load_img(path, target_size=(320, 240))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    classes = model.predict(x)
    print(classes)

    recognized_result = format(class_names[np.argmax(classes)])

    print(f'{img_name[:-4]} is {recognized_result}')


for img in images:
    predict_img1(img)

# predict_img1('HC06.png')

