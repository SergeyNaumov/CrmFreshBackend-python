import os
import re
import random
from base64 import b64decode
from datetime  import datetime


def generate_filename(image_format):
    current_date = datetime.now().strftime('%Y%m%d')
    random_number = random.randint(1000, 9999)
    return f"{current_date}_{random_number}.{image_format}"

def save_images_and_replace_links(html_content, save_dir, save_html_dir):
    def replacement(match):
        image_format = match.group(1)
        base64_data = match.group(2)

        # Генерируем имя файла
        file_name = generate_filename(image_format)
        file_path = os.path.join(save_dir, file_name)

        # Декодируем данные и сохраняем файл

        with open(file_path, 'wb') as img_file:
            img_file.write(b64decode(base64_data))

        # Возвращаем новую ссылку на изображение

        return f'{save_html_dir}/{file_name}'


    pattern = re.compile(r'src="data:image/(\w+);base64,([a-zA-Z0-9+/=]+)"')

    # Заменяем все вхождения изображений в HTML
    #new_html_content = pattern.sub(lambda m: f'<img src="{save_html_dir}/{replacement(m)}">', html_content)

    # Убираем лишние части от старых тегов img
    #new_html_content = re.sub(r"data:image/\w+;base64,[a-zA-Z0-9+/=]+'>", "'>", new_html_content)
    new_html_content = pattern.sub(lambda m: f'src="{replacement(m)}"', html_content)

    return new_html_content

async def wysiwyg_before_save(form,field,value):
    """
    Ищем в коде картинки вида <img src="data:image/png;base64,...">
    и сохраняем их
    """
    base64_save_dir=field.get('base64_save_dir')
    base64_save_dir_html=field.get('base64_save_dir_html')

    if not(base64_save_dir) or not(base64_save_dir_html):
        return value

    # Создаем директорию, если она не существует
    os.makedirs(base64_save_dir, exist_ok=True)

    # Регулярное выражение для поиска данных в формате base64


    new_value = save_images_and_replace_links(value, base64_save_dir, base64_save_dir_html)
    return new_value
