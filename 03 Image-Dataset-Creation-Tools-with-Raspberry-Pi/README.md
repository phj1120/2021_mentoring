# 2021 1학기 홈네트워크 프로젝트

## 환경
```bash
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

### 01 subscribe_raspberry_pi.py

* 라즈베리파이에서 실행시키는 코드

* controller, controller_easy 로 신호 보내면 촬영 시작


### 02 subscribe_pc.py

* PC 에서 실행시키는 코드

* controller, controller_easy 실행 여부 쉽게 확인하기 위해서 제작

### 03 controller.py

* python 으로 라즈베리파이 컨트롤 하는 코드

### 04 controller_easy.py

* 촬영 진행 중 불편해 더 간단하게 사용할 수 있도록 수정

