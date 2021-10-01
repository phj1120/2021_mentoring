# 2021 1학기 홈네트워크 프로젝트

## 환경
```bash
pip install selnium
pip install paho-mqtt
```


## 구성
* 라즈베리파이 4 B+ 4대
* 파이 카메라 4개
* PC 1대

## 설명
* 이미지 분류 딥러닝 모델을 만드는데 필요한 이미지 원활하게 수집하기 위해 제작
* 파이 카메라 여러대를 이용해 사진 촬영
* MQTT 프로토콜로 카메라 제어

## 소스 코드

### 1. raspberry_pi_subscribe.py

* 라즈베리파이 카메라가 연결된 라즈베리파이에서 실행 할 코드

* MQTT 프로토콜 이용해 대수 제한 없이 원하는 만큼 조작 가능

### 2. control_raspberry_pi.py

* 라즈베리파이 제어

### 3. control_raspberry_pi_easy.py

* 촬영 진행 중 불편해 더 간단하게 사용할 수 있도록 수정
