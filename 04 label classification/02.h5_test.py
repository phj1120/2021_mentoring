# from tensorflow.keras.preprocessing import image 로 하면 오류
# tensorflow 2.6.0 버전에서
# from keras.preprocessing import image 로 임포트 하고 실행하면 정상 작동
#

import os
import time
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, callbacks, models
from tensorflow.keras.applications.vgg16 import VGG16

data_kind = "some_data"
# data_kind = "all_data"
repository_dir = '.'
base_dir = f'{repository_dir}/sensor_img/'
model_dir = f'{base_dir}/model'
img_dir = f'{base_dir}/{data_kind}'
train_dir = f'{img_dir}/train'
test_img_dir = f'{img_dir}/test'
class_dir = f'{img_dir}/train'


# model = models.load_model('model/VGG(sparse_categorical_crossentropy, binary)_all_data_checkpoint_model_2021.07.29. 02.57.33.h5')
# model = models.load_model('model/VGG(categorical_crossentropy, categorical)_all_data_checkout_model_2021.07.28. 18.04.36.h5')

# model.summary()

def my_predict(model_path):
    my_model = models.load_model(model_path)
    test_lists = os.listdir(test_img_dir)
    # predict_result =[]
    predict_result = {}
    total_correct = total_count = 0
    for idx, test_list in enumerate(test_lists):
        correct = wrong = 0
        print(idx, test_list)
        test_imgs = os.listdir(f'{test_img_dir}/{test_list}')
        for test_img in test_imgs:
            path = f'{test_img_dir}/{test_list}/{test_img}'
            img = image.load_img(path, target_size=(320, 240))

            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            classes = my_model.predict(x)
            class_names = sorted(os.listdir(class_dir))
            recognized_result = format(class_names[np.argmax(classes)])
            if test_list == recognized_result:
                correct += 1
                print(
                    f'{test_list.upper() == recognized_result.upper()} {correct} : {test_img[:-4]} is {recognized_result}')
            else:
                wrong += 1
                print(
                    f'{test_list.upper() == recognized_result.upper()} {wrong} : {test_img[:-4]} is {recognized_result}')
            total_count += 1
        total_correct += correct
        predict_result[recognized_result] = correct / len(test_imgs)
        # predict_result.append(correct/len(test_imgs))
        print(f'{test_list} predict result : {predict_result[recognized_result]}')

    total_result = f'total : {total_correct / total_count}'
    print(total_result)
    return predict_result, total_result


model_lists = os.listdir(model_dir)
model_predict_result = {}
model_predict_total_result = {}

for model in model_lists:
    if os.path.isfile(f'{model_dir}/{model}'):
        result, total_result = my_predict(f'{model_dir}/{model}')

        model_predict_result[model] = result
        model_predict_total_result[model] = total_result

        print(model_predict_result)
        print(model_predict_total_result)

for key, val in model_predict_result.items():
    print(f" {key} : {val}")

for key, val in model_predict_total_result.items():
    print(f" {key} : {val}")