from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

from module.voice_text import speak

def search(keyword) :
    speak("검색중입니다")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get('https://www.naver.com/')

    time.sleep(1)

    search_input = driver.find_element(By.CSS_SELECTOR, '#query')
    search_input.send_keys(keyword)

    search_btn = driver.find_element(By. CSS_SELECTOR, '#search-btn')
    search_btn.click()

    time.sleep(3)

    driver.quit()
    speak("검색 기능을 종료합니다")



    