#!/usr/bin/env python


import os
import math
from PIL import Image
#input_dir = './females/';suffix = 'f'
input_dir = './males/';suffix = 'm'
output_dir = './processed/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', 'heic', 'webp')):
        with Image.open(os.path.join(input_dir, filename)) as img:
            resized_img = img.resize((128, 128), Image.BICUBIC)

            out_filename = f'128x128_{suffix}_{filename}'

            resized_img.save(os.path.join(output_dir, out_filename))
            print(f"Обработан: {filename}")
