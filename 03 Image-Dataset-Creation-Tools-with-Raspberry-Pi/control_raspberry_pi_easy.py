import paho.mqtt.client as mqtt


# input only int
def input_number():
    try:
        num = int(input('장수 : '))
        return num
    except ValueError:
        print('정수 입력')
        return input_number()


# Input & Publish Message
def input_pub_message():
    while True:
        sensor_name = input('이름 : ')
        client_raspberrypi_pub.publish("RaspberryPi/SensorName", sensor_name)
        number = input_number()
        client_raspberrypi_pub.publish("RaspberryPi/CaptureNumber", number)
        print(f"{sensor_name} : {number} 장 촬영")


# Publish Message
def num_pub_message(name):
    client_raspberrypi_pub.publish("RaspberryPi/SensorName", name)
    print(f'이름 : {name}')
    while True:
        number = input_number()
        client_raspberrypi_pub.publish("RaspberryPi/CaptureNumber", number)
        print(f"{name} : {number} 장 촬영")


# Publish Message
def easy_pub_message(name, num):
    client_raspberrypi_pub.publish("RaspberryPi/SensorName", name)
    client_raspberrypi_pub.publish("RaspberryPi/CaptureNumber", num)
    print(f"{name} : {num} 장 촬영")


# Publish Camera Signal & Sensor Name
client_raspberrypi_pub = mqtt.Client("raspberrypi_subscriber")
client_raspberrypi_pub.connect("test.mosquitto.org", 1883,60)
client_raspberrypi_pub.loop_start()

name = 'Keypad'
num = 250


# 연속 촬영시 전과 동일한 장수 촬영 불가

# 위의 값으로 1회 전송
# easy_pub_message(name, num)

# 위의 name 으로 촬영 회수 반복 전송
num_pub_message(name)

# 이름, 회수 반복 전송
# input_pub_message()