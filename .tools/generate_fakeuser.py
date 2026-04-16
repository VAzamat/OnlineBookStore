#!/usr/bin/env python

####
# %run generate_fakeuser.py
####

import os
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from faker import Faker
import string
import random

fake = Faker('en_US')
input_dir = './128x128/'

User.objects.filter(is_superuser=False).delete()

password_chars = string.ascii_letters + string.digits + "!@#$%^&*()"

suffix =  ["+promo", "+book"] + 2* ["+shop"] + 30 * [""]
email_domains = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com',
    'protonmail.com', 'mail.com', 'zoho.com', 'aol.com', 'gmx.com',
    'fastmail.com', 'hushmail.com', 'tutanota.com', 'rocketmail.com', 'yandex.com',
    'yandex.ru', 'bk.ru', 'inbox.ru',            # RU
    'web.de', 'gmx.de', 't-online.de',           # DE (Германия)
    'orange.fr', 'free.fr', 'laposte.net',       # FR (Франция)
    'libero.it', 'virgilio.it',                  # IT (Италия)
    'seznam.cz',                                 # CZ (Чехия)
    'naver.com'                                  # KR (Корея)
]

def generate_email(first_name, last_name, i=random.randint(1,5)):
    f = first_name.lower().replace("'", "")
    l = last_name.lower().replace("'", "")

    variants = [
        f"{f}_{l}_{get_random_string(4, '0123456789')}",
        f"{f[0]}_{l}_{get_random_string(i, 'abcdefghijklmnopqrstuvwxyz')}",
        f"{f[0]}.{l}_{get_random_string(i, 'abcdefghijklmnopqrstuvwxyz0123456789abcdef')}",
        f"{l[0]}_{f}_{get_random_string(i, '0123456789abcdef')}",
        f"{l[0]}.{f}_{get_random_string(i, 'abcdefghijklmnopqrstuvwxyz')}",
        f"{l}-{f}",
        f"{f}_{l[0]}_{get_random_string(i, '0123456789abcdefghijklmnopqrstuvwxyz')}"
    ]
    return random.choice(variants)+random.choice(suffix)+"@"+random.choice(email_domains)

if not os.path.exists(input_dir):
    print(f"Ошибка: Директория {input_dir} не найдена.")
else:
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):

            # Определяем пол по вхождению подстроки в имени файла
            if '_f_' in filename.lower():
                first_name = fake.first_name_female()
                last_name = fake.last_name_female()
            elif '_m_' in filename.lower():
                first_name = fake.first_name_male()
                last_name = fake.last_name_male()
            else:
                # Пропускаем файл, если пол не указан в названии
                continue


            # Генерируем случайный пароль
            raw_password = get_random_string(12, allowed_chars=password_chars)

            username = fake.unique.user_name()
            email = generate_email(first_name, last_name) #fake.unique.email()

            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=raw_password
            )
            print(f"Файл: {filename} -> Создан: {username} ({first_name} {last_name}) | Pass: {raw_password} | {email}")

    print("\nОбработка завершена.")

