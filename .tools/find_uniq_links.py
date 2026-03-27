#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
from pathlib import Path

# Директория с вашими приложениями (bookshelf, blog, orders и т.д.)
base_dir = Path('.') 
unique_links = set()

# Рекурсивный поиск всех .html файлов
for html_file in base_dir.rglob('*.html'):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        # Находим все теги <a> с атрибутом href
        for a in soup.find_all('a', href=True):
            link = a['href']
            # Игнорируем пустые ссылки и якоря
            if link and link not in ['#', 'javascript:void(0);']:
                unique_links.add(link)

# Вывод результата
print(f"Найдено уникальных ссылок: {len(unique_links)}")
for link in sorted(unique_links):
    print(f'sed -i "s|href=\\"{link}\\"|href=\\"{{% url \'core:blog_with_sidebar\' %}}\\"|g" *.html')