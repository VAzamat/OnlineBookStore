#!/usr/bin/env python

import os
import re
import time
from deep_translator import GoogleTranslator  # pip install deep-translator

# Настройки\
TEMPLATE_DIR = './templates'
SED_FILE = 'replace_trans.sed'
PO_FILE = 'django.po'

translator = GoogleTranslator(source='auto', target='ru')
pattern = re.compile(r'>\s*([A-Za-z][^<>{}\n\r]+?)\s*<')


def generate_i18n_files():
    found_phrases = set()

    # 1. Собираем все уникальные английские фразы
    for root, dirs, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith('.html'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    matches = pattern.findall(f.read())
                    for m in matches:
                        if m.strip(): found_phrases.add(m.strip())

    if not found_phrases:
        print("Фразы не найдены.")
        return

    sorted_phrases = sorted(list(found_phrases), key=len, reverse=True)


    # 2. Генерация SED и PO
    print(f"Начинаю обработку {len(sorted_phrases)} фраз...")
    po_output_text = ""
    sed_output_text = ""

    for eng_text in sorted_phrases:
        try:
            ru_text = translator.translate(eng_text)

            # Экранирование для sed
            safe_eng = eng_text.replace('/', r'\/').replace('&', r'\&').replace('"', r'\"')

            # 1. Запись в SED (только оборачивает в транслятор, оставляет английский)
            # s/>Welcome</>{% trans "Welcome" %}</g
            sed_output_text += f's/>{safe_eng}</>{{% trans "{safe_eng}" %}}</g\n'


            # 2. Запись в PO (связка English -> Russian)
            po_output_text += f"""
msgid "{eng_text}"
msgstr "{ru_text}"

"""
            print(f"Готово: {eng_text[:40]}...")
            time.sleep(0.7)
        except Exception as e:
            print(f"Ошибка: {eng_text} -> {e}")

    # 3. Запись в файлы  SED и PO на диске
    with open(SED_FILE, 'w', encoding='utf-8') as sed_f:
        sed_f.write( sed_output_text )

    with open(PO_FILE, 'w', encoding='utf-8') as po_f:
        # Заголовок для .po файла
        po_f.write('msgid ""\nmsgstr ""\n"Content-Type: text/plain; charset=UTF-8\\n"\n\n')
        po_f.write( po_output_text )


    print(f"\nЗавершено успешно!")
    print(f"1. Примените sed: find {TEMPLATE_DIR} -name '*.html' -exec sed -i -f {SED_FILE} {{}} +")
    print(f"2. Положите {PO_FILE} в locale/ru/LC_MESSAGES/ и выполните python manage.py compilemessages")


if __name__ == "__main__":
    generate_i18n_files()
