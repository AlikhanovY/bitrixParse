# from time import sleep
# from bs4 import BeautifulSoup
# from login import login_to_bitrix
#
# driver = login_to_bitrix()
#
# # Получаем HTML и создаём soup
# html = driver.page_source
# soup = BeautifulSoup(html, "html.parser")
#
# # Находим карточки статей
# cards = soup.select(".landing-item")
# article_data = []
#
# for card in cards:
#     title_elem = card.select_one(".landing-title-overflow")
#     link_elem = card.select_one("a.landing-item-link")
#
#     title = title_elem.get_text(strip=True) if title_elem else "Без названия"
#     url = link_elem["href"] if link_elem and link_elem.has_attr("href") else None
#
#     if url:
#         print(f"▶ Переход к статье: {title}")
#         driver.get(url)
#         sleep(2)
#
#         inner_soup = BeautifulSoup(driver.page_source, "html.parser")
#         content_blocks = inner_soup.select(".landing-block-node-title, .landing-block-node-text")
#
#         content = "\n".join(block.get_text(strip=True) for block in content_blocks)
#         article_data.append((title, url, content))
#
#
# with open("bitrix_full_articles.txt", "w", encoding="utf-8") as f:
#     for title, url, content in article_data:
#         f.write(f"\n=== {title} ===\nURL: {url}\n\n{content}\n")
#
# print("✅ Готово! Все статьи собраны.")
# input("Нажми Enter, чтобы закрыть браузер...")
# driver.quit()

import os
import json
from bs4 import BeautifulSoup

# Папки
source_dir = "./final_articles"
output_dir = "./final_texts"

# Создание директории для текстов
os.makedirs(output_dir, exist_ok=True)

# Обход всех JSON-файлов
for filename in os.listdir(source_dir):
    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(source_dir, filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileExistsError:
        continue  # если файл битый

    # Получение заголовка
    title = data.get("TITLE", "Без названия").strip()
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    if not safe_title:
        safe_title = filename.replace('.json', '')

    # Извлечение текста
    blocks = data.get("BLOCKS", {})
    if not isinstance(blocks, dict):
        continue

    text_parts = []
    for block in blocks.values():
        nodes = block.get("nodes", {})
        html_list = nodes.get(".landing-block-node-text", [])
        for html in html_list:
            soup = BeautifulSoup(html, "html.parser")
            clean_text = soup.get_text().strip()
            if clean_text:
                text_parts.append(clean_text)

    full_text = "\n\n".join(text_parts).strip()
    if not full_text:
        continue

    # Запись текста в файл
    output_path = os.path.join(output_dir, f"{safe_title}.txt")
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(full_text)

print("✅ Все тексты сохранены в папку:", output_dir)
