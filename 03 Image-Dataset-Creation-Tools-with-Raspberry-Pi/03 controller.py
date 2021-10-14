# -*- coding: utf-8 -*-
# 라즈베리파이

import paho.mqtt.client as mqtt
import threading

camera_signal_message = " "


# RaspberryPi Subscribe
def on_connect_raspberrypi_sub(client, userdata, flags, rc):
    client_raspberrypi_sub.subscribe("RaspberryPi/Count")


def on_message_raspberrypi_sub(client, userdata, message):
    global camera_signal_message
    camera_signal_message = int(message.payload.decode('utf-8'))
    print(camera_signal_message)


client_raspberrypi_sub = mqtt.Client("raspberrypi_publisher")
client_raspberrypi_sub.connect("test.mosquitto.org", 1883, 60)
client_raspberrypi_sub.on_connect = on_connect_raspberrypi_sub
client_raspberrypi_sub.on_message = on_message_raspberrypi_sub
client_raspberrypi_sub.loop_start()


# Input & Publish Message
def pub_message():
    signal = "RENAME"
    while True:
        if signal == "RENAME":
            print("\n센서 이름을 지정해주세요.")
            sensor_name = input('이름 : ')
            print("")
            client_raspberrypi_pub.publish("RaspberryPi/SensorName", sensor_name)
            signal = ""

        elif signal == "ON":
            client_raspberrypi_pub.publish("RaspberryPi/CameraSignal", "ON")
            print("촬영 시작\n")

        elif signal == "OFF":
            client_raspberrypi_pub.publish("RaspberryPi/CameraSignal", "OFF")
            print("촬영 종료\n")
        elif signal == "COUNT":
            number = input('원하는 장수를 입력헤 주세요 ')
            client_raspberrypi_pub.publish("RaspberryPi/CaptureNumber", number)
            print("신호 보냄\n\n")

        else:
            print("정해진 값을 입력해주세요")

        if signal != "RENAME":
            print("센서 이름 재지정 : RENAME")
            print("   촬영 시작    : ON")
            print("   촬영 종료    : OFF")
            print("  원하는 장수   : COUNT")
            print("  프로그램 종료  : EXIT\n")

        signal = input('신호 : ')


# Publish Camera Signal & Sensor Name
client_raspberrypi_pub = mqtt.Client("raspberrypi_subscriber")
client_raspberrypi_pub.connect("test.mosquitto.org", 1883, 60)

# Threading Input & Publish message
t1 = threading.Thread(target=pub_message)
t1.start()