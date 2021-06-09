import sqlite3
import datetime


def create_table():
    # создание бд
    with sqlite3.connect("news_bd_saved_with_sqlite.db") as db:
        cursor = db.cursor()

        # удаление таблицы
        # cursor.execute("""DROP TABLE IF EXISTS news""")
        # db.commit()

        # создание таблицы
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS news(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link TEXT,
        title TEXT,
        content TEXT,
        publish_date TEXT,
        parsing_date DATE
        );""")
        db.commit()


def insert_news(col1, col2, col3, col4):
    # вставка в таблицу бд
    with sqlite3.connect("news_bd_saved_with_sqlite.db") as db:
        cursor = db.cursor()
        data_list = (col1, col2, col3, col4, datetime.datetime.now())
        cursor.execute("""INSERT INTO news (link, title, content, publish_date, parsing_date) 
                            VALUES (?, ?, ?, ?, ?);""", data_list)
        db.commit()


def check_news(title):
    # проверка статьи на наличие в базе
    with sqlite3.connect("news_bd_saved_with_sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT title FROM news WHERE title = ? """, (title,))
        result = cursor.fetchall()
        if len(result) == 0:
            #print('[INFO] Такой записи нет')
            return 0
        else:
            print('[X] Такая запись существует')
            return 1


def get_data_from_db():
    # получение данных из бд
    with sqlite3.connect("news_bd_saved_with_sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT title, link, publish_date FROM news""")
        data_set = cursor.fetchall()
        return data_set
