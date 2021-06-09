import requests
from bs4 import BeautifulSoup
import time
import sqlite3
import pandas
import random
# pip install openpyxl
from pandas import ExcelWriter
import bd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

url = 'https://hi-tech.news/'
domen = 'https://hi-tech.news'


r = requests.get(url=url, headers=headers)
soup = BeautifulSoup(r.content, 'html.parser')


#  блок с новостями
news = soup.find_all('a', class_='post-title-a')

# создаем список ссылок на новости
link_news = []
for new in news:
    try:
        link = new.get('href')
    except Exception as ex:
        print(ex)
        link = 'не найдена'
    link_news.append(link)
    #print(link)
print(f'Найдено {len(link_news)} новостей')

# создаем бд
bd.create_table()

# забераем контент новостей переберая ссылки
news_content = []
count = 1
for link in link_news:
    r = requests.get(url=link, headers=headers, timeout=5)
    soup = BeautifulSoup(r.content, 'html.parser')
    # ищем название статьи, текст статьи, дату публикации
    title = soup.h1.get_text(strip=True)
    content = soup.find('div', class_='the-excerpt').get_text(strip=True)
    publish_date = soup.find('div', class_='tile-views').get_text(strip=True)

    print(f'Парсим страницу с новостью:\nЗаголовок: "{title[:30]}..." ({count} из {len(link_news)})')
    count += 1

    # вставляем запись в бд
    try:
        if bd.check_news(title) == 0:
            bd.insert_news(link, title, content, publish_date)
            print('[INFO] Новость добавлена в БД')
    except Exception as ex:
        print('[X] Ошибка вставки данных в бд: ', ex)
        continue
    time.sleep(random.randrange(1, 3))

# запись в бд новостей c помощью пандас
# df = pandas.DataFrame(news_content)
# con = sqlite3.connect("mskit_news2.db")
# con.execute("DROP TABLE IF EXISTS items")
# df.to_sql("items", con, index=False)

# вывод данных с бд
data_set = bd.get_data_from_db()
print(pandas.DataFrame(data_set))

# запись в excel новостей с помощью пандас
df = pandas.DataFrame(data_set)
writer = ExcelWriter('news_excel_saved_with_pandas.xlsx')
ndf = df.rename(columns={0: 'Название статьи', 1: 'Ссылка', 2: 'Дата публикации'})
ndf.to_excel(writer, index=True, sheet_name='Новости')
writer.save()
print(f'Данные сохранены в файл "news.xlsx"')

# запись в бд новостей c помощью пандас
df = pandas.DataFrame(data_set)
con = sqlite3.connect("news_bd_saved_with_pandas.db")
con.execute("DROP TABLE IF EXISTS items")
df.to_sql("news", con, index=False)
print(f'Данные сохранены в бд "news_bd_saved_with_pandas.db"')
