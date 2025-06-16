from time import sleep
from bs4 import BeautifulSoup
from login import login_to_bitrix

driver = login_to_bitrix()

# Получаем HTML и создаём soup
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Находим карточки статей
cards = soup.select(".landing-item")
article_data = []

for card in cards:
    title_elem = card.select_one(".landing-title-overflow")
    link_elem = card.select_one("a.landing-item-link")

    title = title_elem.get_text(strip=True) if title_elem else "Без названия"
    url = link_elem["href"] if link_elem and link_elem.has_attr("href") else None

    if url:
        print(f"▶ Переход к статье: {title}")
        driver.get(url)
        sleep(2)

        inner_soup = BeautifulSoup(driver.page_source, "html.parser")
        content_blocks = inner_soup.select(".landing-block-node-title, .landing-block-node-text")

        content = "\n".join(block.get_text(strip=True) for block in content_blocks)
        article_data.append((title, url, content))


with open("bitrix_full_articles.txt", "w", encoding="utf-8") as f:
    for title, url, content in article_data:
        f.write(f"\n=== {title} ===\nURL: {url}\n\n{content}\n")

print("✅ Готово! Все статьи собраны.")
input("Нажми Enter, чтобы закрыть браузер...")
driver.quit()
