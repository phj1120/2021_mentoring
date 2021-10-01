"""
이미지 한개를 다운로드

1. 패키지 설치
pip install selenium

2. 크롬드라이버
https://chromedriver.chromium.org/downloads
"""

import os
import time
import urllib
from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.common.keys import Keys

# chromedriver 불러오기
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver/93.0.4577.15/chromedriver.exe', options=chrome_options)

# 디렉터리 생성
pwd = os.getcwd()
image_directory = os.path.join(pwd, "image")

try:
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
except OSError:
    print('디렉터리 생성 실패')

# 이미지 크롤링
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")
query = driver.find_element_by_name("q")
keyword = input('수집할 이미지 입력 : ')
query.send_keys(keyword)
query.send_keys(Keys.RETURN)

# 찾는중
driver.find_elements_by_css_selector(".rg_i.Q4LuWd")[0].click()
time.sleep(1)
print("찾는중.")
time.sleep(1)
print("찾는중..")
time.sleep(1)
print("찾는중...")

# 이미지 URL
image_url = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
print("URL :", image_url)

# 확장자
file_extension = image_url.split(".")[-1]

# 이미지 저장
urllib.request.urlretrieve(image_url, "{}/{}.jpg".format(image_directory, keyword))
print("다운로드 완료")
