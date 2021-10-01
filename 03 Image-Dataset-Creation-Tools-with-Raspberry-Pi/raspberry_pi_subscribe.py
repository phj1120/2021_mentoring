# -*- coding: utf-8 -*-
# MQTT 구독
# 카메라가 연결된 라즈베리파이에서 실행

import paho.mqtt.client as mqtt

past_number = 0


# Sensor Name Subscribe
def on_connect_sensor(client, userdata, flags, rc):
    client_sensor.subscribe("RaspberryPi/SensorName")
    print("success connect : sensor name")


def on_message_sensor(client, userdata, message):
    sensor_signal_message = message.payload.decode('utf-8')
    print(f"success recieve sensor name : {sensor_signal_message}")


client_sensor = mqtt.Client()
client_sensor.connect("test.mosquitto.org", 1883, 60)
client_sensor.on_connect = on_connect_sensor
client_sensor.on_message = on_message_sensor
client_sensor.loop_start()


# Count Subscribe
def on_connect_sub_count(client, userdata, flags, rc):
    client_sub_count.subscribe("RaspberryPi/CaptureNumber")
    print("success connect : Caputure Number")


def on_message_sub_count(client, userdata, message):
    global past_number
    number = int(message.payload.decode('utf-8'))
    print(f"success recieve number : {number}")


client_sub_count = mqtt.Client()
client_sub_count.connect("test.mosquitto.org", 1883,60)
client_sub_count.on_connect = on_connect_sub_count
client_sub_count.on_message = on_message_sub_count
client_sub_count.loop_forever()