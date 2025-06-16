import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login_to_bitrix

driver = login_to_bitrix()


article_urls = [
    ("Инструменты", "https://rocketfirmgroup.bitrix24.kz/knowledge/instrumenty/"),
    ("TeachLead", "https://rocketfirmgroup.bitrix24.kz/knowledge/teachlead/"),
    ("Pharm / eDetailing / CLM / EMS", "https://rocketfirmgroup.bitrix24.kz/knowledge/pharm_edetailing_clm_ems/"),
    ("Производство", "https://rocketfirmgroup.bitrix24.kz/knowledge/proizvodstvo/"),
    ("Holy Media", "https://rocketfirmgroup.bitrix24.kz/knowledge/holy_media/"),
    ("SMM", "https://rocketfirmgroup.bitrix24.kz/knowledge/smm/"),
    ("Компания", "https://rocketfirmgroup.bitrix24.kz/knowledge/companiya/"),
    ("Проектный офис", "https://rocketfirmgroup.bitrix24.kz/knowledge/proektnyi_ofis/"),
    ("Бэк-офис", "https://rocketfirmgroup.bitrix24.kz/knowledge/bekofis/"),
    ("Планирование", "https://rocketfirmgroup.bitrix24.kz/knowledge/planirovanie/"),
    ("Ready Bank", "https://rocketfirmgroup.bitrix24.kz/knowledge/ready_bank/")
]

driver.get("https://rocketfirmgroup.bitrix24.kz/knowledge/instrumenty/registratsiyavsisteme/?IFRAME=Y")
try:
    # Ждём появления нужного h2 (заголовок статьи)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//h2[contains(., 'Регистрация по ссылке')]")
        )
    )

    # Статья подгружена — сохраняем весь HTML
    html = driver.page_source
    with open("article_loaded.html", "w", encoding="utf-8") as f:
        f.write(html)

finally:
    driver.quit()







# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.TAG_NAME, "iframe"))
# )
#
# iframe = driver.find_element(By.TAG_NAME, "iframe")
# driver.switch_to.frame(iframe)
#
#
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.TAG_NAME, "ul"))  # Можно уточнить, если нужно
# )
#
# html = driver.page_source
#
# soup = BeautifulSoup(html, 'html.parser')
#
#
# for li in soup.find_all("li"):
#     a = li.find("a")
#     if a:
#         print(a.get_text(strip=True), "→", a.get("href"))
#
# driver.quit()