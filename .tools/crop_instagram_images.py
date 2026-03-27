

import os
import math
from PIL import Image
from pillow_heif import register_heif_opener

# Регистрируем обработчик HEIC в Pillow
register_heif_opener()

# Настройки
angle = -2
input_dir = './sources/'
output_dir = './processed/'

def get_safe_crop_size(width, height, angle_deg):
    # Переводим в радианы
    angle_rad = math.radians(abs(angle_deg))

    # Для квадрата формула упрощается:
    # s = L / (sin(a) + cos(a))
    side = width / (math.sin(angle_rad) + math.cos(angle_rad))
    return int(side)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', 'heic', 'webp')):
        with Image.open(os.path.join(input_dir, filename)) as img:
            # 1. Поворот с высоким качеством (BICUBIC) 
            # expand=False сохраняет размер холста 1080x1080
            rotated = img.rotate(angle, resample=Image.BICUBIC, expand=False)
            # Расчет координат для кропа (вырезаем центр 1000x1000)
            input_size_x, input_size_y = img.size
            output_size = get_safe_crop_size( input_size_x, input_size_y, angle )
            output_size -= 8 #обрезаем еще немного
            left  = (input_size_x - output_size) / 2
            right = (input_size_x + output_size) / 2

            top    = (input_size_y - output_size) / 2
            bottom = (input_size_y + output_size) / 2

            
            # 2. Обрезка центральной части
            final_img = rotated.crop((left, top, right, bottom))
            
            # 3. Сохранение
            out_filename = os.path.splitext(filename)[0] +  ".jpg"

            final_img.save(os.path.join(output_dir, out_filename))
            print(f"Обработан: {filename}")
