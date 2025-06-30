# import os
# import shutil
#
# from bs4 import BeautifulSoup
# import json
#
# folder_path = './LANDING'
#
# useful_files = []
#
# for filename in os.listdir(folder_path):
#     if not filename.endswith('.json'):
#         continue
#
#     filepath = os.path.join(folder_path, filename)
#     with open(filepath, 'r', encoding='utf-8') as f:
#         try:
#             data = json.load(f)
#         except Exception as e:
#             continue  # Пропускаем повреждённые
#
#         blocks = data.get("BLOCKS", {})
#
#         # Пропускаем, если BLOCKS не словарь
#         if not isinstance(blocks, dict):
#             continue
#
#         for block in blocks.values():
#             nodes = block.get("nodes", {})
#             texts = nodes.get(".landing-block-node-text", [])
#             if texts:
#                 has_text = True
#                 break
#
#         if has_text:
#             useful_files.append(filename)
#
# # Выводим нужные файлы
# print("Найдено полезных файлов:", len(useful_files))
# for name in useful_files:
#     print(name)
#
# destination = './filtered_json'
# os.makedirs(destination, exist_ok=True)
#
# for filename in useful_files:
#     shutil.copy(os.path.join(folder_path, filename), destination)

import os
import json
from bs4 import BeautifulSoup

source_folder = './filtered_json'
output_folder = './texts'

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(source_folder):
    if not filename.endswith('.json'):
        continue

    filepath = os.path.join(source_folder, filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception:
            continue

    title = data.get('TITLE', 'no_title').strip()

    # Приводим название к допустимому для файлов имени
    safe_title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not safe_title:
        safe_title = filename.replace('.json', '')

    blocks = data.get('BLOCKS', {})
    if not isinstance(blocks, dict):
        continue

    text_parts = []

    for block in blocks.values():
        nodes = block.get('nodes', {})
        html_list = nodes.get('.landing-block-node-text', [])
        for html in html_list:
            soup = BeautifulSoup(html, 'html.parser')
            text_parts.append(soup.get_text())

    full_text = '\n\n'.join(text_parts).strip()

    if full_text:
        output_path = os.path.join(output_folder, f"{safe_title}.txt")
        with open(output_path, 'w', encoding='utf-8') as out_file:
            out_file.write(full_text)

print("✅ Все статьи сохранены в папку 'texts'.")
