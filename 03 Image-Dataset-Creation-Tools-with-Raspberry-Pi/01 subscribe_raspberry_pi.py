# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import os
import uuid
import threading
from picamera import PiCamera
from time import sleep

capture = False
camera_signal_message = ""
sensor_signal_message = "None"
past_number = 0
count = 0

# RaspberryPi/CameraSignal
# RaspberryPi/SensorName
# RaspberryPi/CaptureNumber
# 각각 구독

# 구독 시 필요한 함수 아래처럼 제작함
# on_connect_camera, on_message_camera
# on_connect_sensor, on_message_sensor
# on_connect_sub_count, on_message_sub_count

# 촬영 중인 장수 발행함(전송)
# pub_count 메서드로
# RaspberryPi/CaptureNumber


# create_folder
# 촬영한 사진 저장 하기 위해 없는 경우 폴더 생성

# shoot_camera
# 사진 저장 위치, 이름 지정, 촬영(한장)

# mqtt_camera
# camera_signal_message 으로 받은 촬영 장 수 만큼
# shoot_camera 실행해서 촬영


# number_of_capture
# on_message_sub_count에 보면 이거 실행하는게 있는데
# 이거 떄문에 전에 보낸 장수랑 같은 장수 촬영 불가
# 아마 이거 했던 이유가
# 한번 발행하면 한번만 전송되는게 아니라 여러번 전송 되었거나
# 한번 발행하고 받아들인 값을 0으로 초기화 안했던지 해서
# 계속 같은 값이 들어와서 촬영이 안멈춰서 이 코드 추가한 거 일 거임


# Camera Signal Subscribe
def on_connect_camera(client, userdata, flags, rc):
    client_camera.subscribe("RaspberryPi/CameraSignal")
    print("success connect : camera signal")


def on_message_camera(client, userdata, message):
    global camera_signal_message
    camera_signal_message = message.payload.decode('utf-8')
    print(("success receive camera signal : " + camera_signal_message))


client_camera = mqtt.Client()
client_camera.connect("test.mosquitto.org", 1883, 60)
client_camera.on_connect = on_connect_camera
client_camera.on_message = on_message_camera
client_camera.loop_start()


# Sensor Name Subscribe
def on_connect_sensor(client, userdata, flags, rc):
    client_sensor.subscribe("RaspberryPi/SensorName")
    print("success connect : sensor name")


def on_message_sensor(client, userdata, message):
    global sensor_signal_message
    sensor_signal_message = message.payload.decode('utf-8')
    print(("success recieve sensor name : " + sensor_signal_message))


client_sensor = mqtt.Client()
client_sensor.connect("test.mosquitto.org", 1883, 60)
client_sensor.on_connect = on_connect_sensor
client_sensor.on_message = on_message_sensor
client_sensor.loop_start()


# Count Subscribe
def on_connect_sub_count(client, userdata, flags, rc):
    client_sub_count.subscribe("RaspberryPi/CaptureNumber")
    print("success connect : Caputur Number")


def on_message_sub_count(client, userdata, message):
    global past_number
    number = int(message.payload.decode('utf-8'))
    if past_number != number:
        print("past number : " + str(past_number) + "number :" + str(number))
        number_of_capture(number)


client_sub_count = mqtt.Client()
client_sub_count.connect("test.mosquitto.org", 1883, 60)
client_sub_count.on_connect = on_connect_sub_count
client_sub_count.on_message = on_message_sub_count
client_sub_count.loop_start()


# Count Publish
def pub_count():
    global count
    count += 1
    client_count.publish("RaspberryPi/CaptureNumber", count)


client_count = mqtt.Client()
client_count.connect("test.mosquitto.org", 1883, 60)
client_count.loop_start()


# Shooting Camera
def create_folder(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def shoot_camera():
    global sensor_signal_message

    sensor_name = sensor_signal_message
    file_name = uuid.uuid4().hex
    folder_path = '/home/pi/Project/' + sensor_name
    create_folder(folder_path)
    file_path = folder_path + '/' + file_name + '.jpg'
    camera.capture(file_path)
    print(('Saving : ' + file_path))


def mqtt_camera():
    global camera_signal_message, count
    while True:
        if camera_signal_message == "ON":
            shoot_camera()
            count += 1
        elif camera_signal_message == "OFF":
            print('Final Count : ' + str(count))
            print("Camera OFF")
            camera_signal_message = ""
        sleep(0.1)


def number_of_capture(number):
    global past_number
    past_number = number
    sleep(0.1)

    i = 0
    while True:
        shoot_camera()
        i += 1
        if (number <= i):
            break
        sleep(0.1)


camera = PiCamera()
camera.resolution = (240, 160)

t1 = threading.Thread(target=mqtt_camera)
t1.start()

