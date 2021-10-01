import os
import time
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras import layers, callbacks
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def my_train(data_kind, my_loss, my_class_mode, my_epochs):
    repository_dir = '.'
    base_dir = f'{repository_dir}/sensor_img/'
    model_dir = f'{base_dir}/model'
    img_dir = f'{base_dir}/{data_kind}'
    test_img_dir = f'{base_dir}/test/{data_kind}'

    train_dir = f'{img_dir}/train'
    validation_dir = f'{img_dir}/validation'

    print(os.listdir(train_dir))
    print(os.listdir(validation_dir))

    # Add our data-augmentation parameters to ImageDataGenerator
    # train_datagen = ImageDataGenerator(rescale = 1./255.,rotation_range = 40, width_shift_range = 0.2, height_shift_range = 0.2, shear_range = 0.2, zoom_range = 0.2, horizontal_flip = True)
    train_datagen = ImageDataGenerator(rescale = 1./255. )

    # Note that the validation data should not be augmented!
    test_datagen = ImageDataGenerator( rescale = 1.0/255. )

    # Flow training images in batches of 20 using train_datagen generator
    train_generator = train_datagen.flow_from_directory(train_dir, batch_size = 20, class_mode = my_class_mode, target_size = (320, 240))

    # Flow validation images in batches of 20 using test_datagen generator
    validation_generator = test_datagen.flow_from_directory( validation_dir,  batch_size = 20, class_mode = my_class_mode, target_size = (320, 240))


    base_model = VGG16(input_shape = (320, 240, 3), # Shape of our images
        include_top = False, # Leave out the last fully connected layer
        weights = 'imagenet')

    # 모든 레이어를 훈련할 필요가 없으므로
    for layer in base_model.layers:
        layer.trainable = False

    # Flatten the output layer to 1 dimension
    x = layers.Flatten()(base_model.output)

    # Add a fully connected layer with 512 hidden units and ReLU activation
    x = layers.Dense(512, activation='relu')(x)

    # Add a dropout rate of 0.5
    x = layers.Dropout(0.5)(x)

    # Add a final sigmoid layer for classificatio
    # 데이터 종류에 맞게 마지막 dense 층 설정
    x = layers.Dense((12 if data_kind=='all_data' else 5) , activation='softmax')(x)

    model = tf.keras.models.Model(base_model.input, x)

    model.compile(optimizer = tf.keras.optimizers.RMSprop(lr=0.0001), loss=my_loss, metrics = ['acc'])

    now = time.localtime()
    now_time = "%04d.%02d.%02d. %02d.%02d.%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    # val_loss 가능, 가장 좋은 값 저장
    my_save = callbacks.ModelCheckpoint(
        f'{model_dir}/VGG({my_loss}, {my_class_mode})_{data_kind}_checkout_model_{now_time}.h5',
        monitor='val_accuracy')

    # 학습 정체시 학습률 줄이기
    my_rate = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5,
                                          patience=20)

    hist = model.fit(train_generator, validation_data = validation_generator,
                        callbacks = [my_save, my_rate],
                        # steps_per_epoch = 100,
                        batch_size = 512,
                        epochs = my_epochs)

    model.save(f'{model_dir}/VGG({my_loss}, {my_class_mode})_{data_kind}_model.h5')


    class_names = sorted(os.listdir(train_dir))
    print(class_names)

    def predict_img(img_name):
        path = (f'{test_img_dir}/{img_name}')
        img = image.load_img(path, target_size=(320, 240))

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])

        classes = model.predict(x)
        recognized_result = format(class_names[np.argmax(classes)])

        print(f'{img_name[:-4].upper() == recognized_result.upper()} : {img_name[:-4]} is {recognized_result}')


    images = os.listdir(test_img_dir)

    for img in images:
        predict_img(img)

    fig, loss_ax = plt.subplots()

    acc_ax = loss_ax.twinx()

    loss_ax.plot(hist.history['loss'], 'y', label='train loss')
    loss_ax.plot(hist.history['val_loss'], 'r', label='val loss')

    acc_ax.plot(hist.history['acc'], 'b', label='train acc')
    acc_ax.plot(hist.history['val_acc'], 'g', label='val acc')

    loss_ax.set_xlabel('epoch')
    loss_ax.set_ylabel('loss')
    acc_ax.set_ylabel('accuray')

    loss_ax.legend(loc='upper left')
    acc_ax.legend(loc='lower left')

    plt.show()

# data_kind = "some_data"
# data_kind = "all_data"

# my_loss='categorical_crossentropy'
# my_class_mode = 'categorical'

# my_loss = 'sparse_categorical_crossentropy'
# my_class_mode = 'binary'

# my_train(data_kind, my_loss, my_class_mode):
# my_train('all_data', 'sparse_categorical_crossentropy', 'binary', 100)

my_train('all_data', 'categorical_crossentropy', 'categorical', 200)