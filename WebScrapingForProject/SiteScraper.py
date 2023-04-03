import csv
import re

from bs4 import BeautifulSoup
import requests

url = 'http://anglicismdictionary.ru/Slovar'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.4.779 Yowser/2.5 Safari/537.36"
}


req = requests.get(url=url,
                   headers=headers
                   )
src = req.text

with open('pages/main.html', 'w', encoding='utf-8') as file:
    file.write(src)


# Считываем скешированный файл для получения элементов со ссылками
with open('main.html', 'r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')
rows_letters = soup.find(class_='content').find('table').find('tbody').findAll('tr')


# Получение словаря ссылок
letters_urls = {}
for row in rows_letters:
    prefix = 'http://anglicismdictionary.ru'
    temp_letters_urls = {item.find('a')['href'][1:]: f"{prefix + item.find('a')['href']}" for item in row.findAll('td') if item.find('a')}
    letters_urls: dict = letters_urls | temp_letters_urls


# Заголовок csv файла в итоговый файл
with open('common.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(
        (
            'Word',
            'Origin',
            'Description',
            'Explanation'
        )
    )


error_count = 0
pattern = re.compile(r"\s*([А-ЯЁA-Z].*?)\s?\((.*?)\)\.?.+?(\b[а-яё].*?)?(\b[А-ЯЁA-Z].*)", flags=re.MULTILINE)


for k, v in letters_urls.items():
    src = requests.get(v, headers).text
    # Кеширование страницы
    with open(f'pages/{k}_page.html', 'w', encoding='utf-8-sig') as file:
        file.write(src)

    with open(f'pages/{k}_page.html', 'r', encoding='utf-8-sig') as file:
        data = file.read()

    # Парсинг каждой страницы
    soup = BeautifulSoup(data, 'lxml')
    articles = soup.find(class_='content').findAll('p')
    for article in articles:
        article_str = article.get_text()
        try:
            article_tuple = pattern.match(article_str).groups()  # Парсинг по паттерну
        except AttributeError as er:
            print(f'Ошибка {er}-{error_count} в: {article_str}')
            error_count += 1

        # Запись в итоговый файл
        with open('common.csv', 'a', encoding='utf-8-sig', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(article_tuple)


