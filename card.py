import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login_to_bitrix

url = "https://rocketfirmgroup.bitrix24.kz/knowledge/instrumenty/"
driver = login_to_bitrix()
time.sleep(2)

driver.get(url)


iframe = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "iframe"))
)

driver.switch_to.frame(iframe)

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body > *"))
)
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')
menu_ul = soup.find('ul', class_='landing-block-node-menu')


def extract_leaf_links(ul_tag):
    links = []
    for li in ul_tag.find_all("li", recursive=False):
        a_tag = li.find("a", href=True)
        nested_ul = li.find("ul")

        if a_tag and not nested_ul:
            href = a_tag["href"]
            title = a_tag.get_text(strip=True)
            links.append((title, href))


        if nested_ul:
            links.extend(extract_leaf_links(nested_ul))
    return links

all_links = extract_leaf_links(menu_ul)

for name, link in all_links:
    print(f"{name} -> {link}")


link1 = all_links[1][1]
driver.get(link1)
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, "landing-block-node-text"))
)

html = driver.page_source
driver.switch_to.frame(iframe)

with open('article.html', 'w') as f:
    f.write(html)


# if menu_ul:
#     for a_tag in menu_ul.find_all('a', href=True):
#         text = a_tag.get_text(strip=True)
#         href = a_tag['href']
#         links.append((text, href))
#
#
# link1 = links[2][1]
# driver.get(link1)
# html = driver.page_source
#
# with open('article.html', 'w') as f:
#     f.write(html)
# print(link1)
# for name, link in links:
#     print(f"{name} -> {link}")







