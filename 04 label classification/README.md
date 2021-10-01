# VGG16 커스텀 훈련

## 환경 구성
```bash
pip install tensorflow==2.2.0
pip install keras
pip install matplotlib
```

## 설명
훈련의 편의를 위해 데이터를 두 종류로 나눔
* some_date : 테스트 데이터
* all_data  : 본 데이터

### 01.train
훈련시 변경 가능한 매개변수
```python
compile : loss='categorical_crossentropy',
datagen.flow_from_directory : class_mode='categorical'
```
```python
compile : loss='sparse_categorical_crossentropy'
datagen.flow_from_directory : class_mode='binary'
```

### 02.h5_test
tensorflow==2.6.0 환경에서 진행할 경우 실행 가능하지만
PC에서 기존 설치된 CUDA 사용하기 위해 2.2.0 환경에서 실행해 오류 발생함
```python
from keras.preprocessing import image
```

### 03.convert
h5 로 저장된 모델을 tflite 로 변환하여 저장

### 04.tflite_test
저장된 모델들을 활용해 
{데이터형식}/test 폴더에 있는 이미지 테스트

모델 폴더에 있는 모델들 전부 활용해 훈련 후 각각의 정확도 출력
```python
{'VGG(categorical_crossentropy, categorical)_all_data_checkout_model_2021.09.25. 10.57.01.tflite': {'FZ2904': 1.0, 'LED': 0.99, 'HCSR04': 0.95, 'KEYPAD': 0.83, 'KY026': 0.97, 'LCD KEYPAD SHIELD': 1.0, 'LCD1602': 0.81, 'PM2008': 1.0, 'PPD42NS': 0.89, 'RFID': 0.25, 'SG90': 1.0}, 'VGG(categorical_crossentropy, categorical)_some_data_checkout_model_2021.09.25. 00.40.08.tflite': {'FZ2904': 1.0, 'LED': 0.99, 'HCSR04': 0.95, 'KEYPAD': 0.83, 'KY026': 0.97, 'LCD KEYPAD SHIELD': 1.0, 'LCD1602': 0.81, 'PM2008': 1.0, 'PPD42NS': 0.89, 'RFID': 0.25, 'SG90': 1.0}}
{'VGG(categorical_crossentropy, categorical)_all_data_checkout_model_2021.09.25. 10.57.01.tflite': 'total : 0.815', 'VGG(categorical_crossentropy, categorical)_some_data_checkout_model_2021.09.25. 00.40.08.tflite': 'total : 0.815'}
 VGG(categorical_crossentropy, categorical)_all_data_checkout_model_2021.09.25. 10.57.01.tflite : {'FZ2904': 1.0, 'LED': 0.99, 'HCSR04': 0.95, 'KEYPAD': 0.83, 'KY026': 0.97, 'LCD KEYPAD SHIELD': 1.0, 'LCD1602': 0.81, 'PM2008': 1.0, 'PPD42NS': 0.89, 'RFID': 0.25, 'SG90': 1.0}
 VGG(categorical_crossentropy, categorical)_some_data_checkout_model_2021.09.25. 00.40.08.tflite : {'FZ2904': 1.0, 'LED': 0.99, 'HCSR04': 0.95, 'KEYPAD': 0.83, 'KY026': 0.97, 'LCD KEYPAD SHIELD': 1.0, 'LCD1602': 0.81, 'PM2008': 1.0, 'PPD42NS': 0.89, 'RFID': 0.25, 'SG90': 1.0}
 VGG(categorical_crossentropy, categorical)_all_data_checkout_model_2021.09.25. 10.57.01.tflite : total : 0.815
 VGG(categorical_crossentropy, categorical)_some_data_checkout_model_2021.09.25. 00.40.08.tflite : total : 0.815
```

## 한계점
* 값을 바꿔가며 훈련해봐도 같이 예측을 못하는 것(위의 경우 RFID)이 하나 이상은 있는데 이유를 모르겠음
* 다른 tflite 파일들 처럼 용량 작게 만드는 방법 모르겠음
