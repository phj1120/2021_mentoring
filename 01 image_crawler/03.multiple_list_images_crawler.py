"""
이미지 여러개를 다운로드

1. 패키지 설치
pip install selenium

2. 크롬드라이버
https://chromedriver.chromium.org/downloads
"""

import os
import time
import uuid
import urllib
from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys

# chromedriver 불러오기
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('../chromedriver/93.0.4577.15/chromedriver.exe', options=chrome_options)

# 크롤링 할 이미지
keys = ['HC-SR04', 'DHT11', 'KY-026']

def makedir(keyword):
    pwd = os.getcwd()
    image_directory = os.path.join(pwd, "images", keyword)

    try:
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
    except OSError:
        print('디렉터리 생성 실패')
    return image_directory

def crawling_images(keyword):
    # 디렉터리 생성
    image_directory = makedir(keyword)

    # 이미지 크롤링
    print(f'{keyword} 크롤링 시작')
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
    query = driver.find_element_by_name("q")
    # keyword = input('수집할 이미지 입력 : ')
    query.send_keys(keyword)
    query.send_keys(Keys.RETURN)

    # 이미지를 최대로 찾기 위해서 스크롤을 계속 아래로 내림
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        print("이미지를 최대로 찾기 위해서 스크롤을 아래로 내리는 중")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click()
            except:
                break

        last_height = new_height

    # 이미지 태그 클래스
    images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

    # 이미지 다운로드
    count = 1
    for image in images:
        try:
            image.click()
            image_url = driver.find_element_by_xpath(
                "/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img").get_attribute(
                "src")

            # 파일명
            file_name = uuid.uuid4()

            # 이미지 저장
            urllib.request.urlretrieve(image_url, f'{image_directory}/{file_name}.jpg')
            print(f"{keyword} : {count}개 저장완료")
            count = count + 1
        except:
            pass

    print("다운로드 완료")

for key in keys:
    crawling_images(key)

print("크롤링 완료")