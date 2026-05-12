from bs4 import BeautifulSoup

def html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    def convert_element(element):
        if element.name is None:
            return element.string or ''

        # Обработка заголовков (h1, h2, ..., h6)
        if element.name.startswith('h') and len(element.name) == 2 and element.name[1].isdigit():
            level = int(element.name[1])
            return f"{'#' * level} {element.get_text().strip()}\n\n"

        if element.name == 'br':
            return f"\n"

        # Обработка параграфов
        if element.name == 'p':
            return f"{element.get_text().strip()}\n\n"

        # Обработка ссылок
        if element.name == 'a' and element.get('href'):
            href = element['href']
            text = element.get_text()
            return f"[{text}]({href})"

        # Обработка жирного текста
        if element.name == 'strong' or element.name == 'b':
            return f"*{element.get_text().strip()}*"

        # Обработка курсива
        if element.name == 'em' or element.name == 'i':
            return f"_{element.get_text().strip()}_"

        # Обработка кода
        if element.name == 'code':
            return f"`{element.get_text().strip()}`"

        # Обработка блока кода
        if element.name == 'pre':
            code = element.get_text().strip()
            return f"```\n{code}\n```"

        # Обработка списков
        if element.name == 'ul':
            items = [f"- {convert_element(li)}" for li in element.find_all('li')]
            return "\n".join(items) + "\n"

        if element.name == 'ol':
            items = [f"{i+1}. {convert_element(li)}" for i, li in enumerate(element.find_all('li'))]
            return "\n".join(items) + "\n"

        # Обработка строковых данных внутри элемента
        return ''.join([convert_element(child) for child in element.children])

    return convert_element(soup)
