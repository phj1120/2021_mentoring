# PC 로 접속해서 라즈베리파이 제어하는 코드

import paho.mqtt.client as mqtt

# input only int
def input_number():
    try:
        num = int(input('장수 : '))
        return num
    except ValueError:
        print('정수 입력')
        return input_number()


# 이름, 회수 반복 전송
def input_pub_message():
    while True:
        # RaspberryPi/SensorName 에 입력한 센서 이름 전송
        sensor_name = input('이름 : ')
        client_raspberrypi_pub.publish("RaspberryPi/SensorName", sensor_name)
        # RaspberryPi/CaptureNumber 에 캡처 할 이미지 장수 전송
        # int 만 입력 받기 위해 input_number 함수 만들어서 이미지 장수 설정
        number = input_number()
        client_raspberrypi_pub.publish("RaspberryPi/CaptureNumber", number)
        # 확인용 로그 출력
        print(f"{sensor_name} : {number} 장 촬영")


# 위의 name 으로 촬영 회수 반복 전송
def num_pub_message(name):
    # RaspberryPi/SensorName 에
    client_raspberrypi_pub.publish("RaspberryPi/SensorName", name)
    print(f'이름 : {name}')
    while True:
        number = input_number()
        client_raspberrypi_pub.publish("RaspberryPi/CaptureNumber", number)
        print(f"{name} : {number} 장 촬영")

# 1회 전송
def easy_pub_message(name, num):
    client_raspberrypi_pub.publish("RaspberryPi/SensorName", name)
    client_raspberrypi_pub.publish("RaspberryPi/CaptureNumber", num)
    print(f"{name} : {num} 장 촬영")


# 왜 이렇게 뭉쳐놨는지는 모르겠다...
# 이름을 client_raspberrypi_pub 이거로 한거는
# 구독이랑 발행 한번에 하려고 이렇게 한 것...같은데
# 기억이 안나...
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