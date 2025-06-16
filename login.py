import os
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
USERNAME = os.getenv("BITRIX_USERNAME")
PASSWORD = os.getenv("BITRIX_PASSWORD")

def login_to_bitrix():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 30)

    driver.get("https://rocketfirmgroup.bitrix24.kz/kb/")

    login_input = wait.until(EC.presence_of_element_located((By.ID, "login")))
    login_input.clear()
    login_input.send_keys(USERNAME)

    continue_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".b24net-login-enter-form__continue-btn")))
    ActionChains(driver).move_to_element(continue_button).click().perform()


    password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']")))
    password_input.send_keys(PASSWORD)

    # Кнопка входа
    login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".b24net-text-btn--call-to-action")))
    ActionChains(driver).move_to_element(login_button).click().perform()

    # Ждём и переходим снова на базу знаний
    sleep(3)
    driver.get("https://rocketfirmgroup.bitrix24.kz/kb/")
    sleep(3)

    return driver