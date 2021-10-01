import tensorflow as tf

repository_dir = '.'
base_dir = f'{repository_dir}/sensor_img/'
model_dir = f'{base_dir}/model'

# 변환하고 싶은 h5 모델 이름 지정
model_name = 'VGG(categorical_crossentropy, categorical)_all_data_checkout_model_2021.09.25. 10.57.01'

model = tf.keras.models.load_model(f"{model_dir}/{model_name}.h5")
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open(f"{model_dir}/tflite/{model_name}.tflite", "wb").write(tflite_model)