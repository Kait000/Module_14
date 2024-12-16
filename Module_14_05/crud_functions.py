import sqlite3

DB_NAME = 'products.db'


def initiate_db():
    """Создаем таблицы Products и Users"""
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Products(
                            id INTEGER PRIMARY KEY, 
                            title TEXT NOT NULL,
                            description TEXT,
                            price INTEGER NOT NULL)"""
                       )
        db.commit()

        cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                            id INTEGER PRIMARY KEY,
                            username TEXT NOT NULL,
                            email TEXT NOT NULL,
                            age INTEGER NOT NULL,
                            balance INTEGER NOT NULL DEFAULT 1000)"""
                       )
        db.commit()


def get_all_products():
    """Возвращаем все записи из таблицы Products"""
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM Products""")
        return cursor.fetchall()


def is_included(username):
    """Возвращаем True если username есть в таблице Users"""
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT COUNT(*) FROM Users WHERE username = ?""", (username,))
        if cursor.fetchone()[0]:
            return True
        else:
            return False


def add_user(username, email, age):
    """Добавление нового пользователя"""
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""INSERT INTO Users (username, email, age) VALUES (?, ?, ?)""",
                       (username, email, age))
        db.commit()


if __name__ == '__main__':
    exit()  # закоментировать для создания БД

    initiate_db()

    items = [
        ('Продукт 1', 'Гематоген', 100),
        ('Продукт 2', 'Активированный уголь', 200),
        ('Продукт 3', 'Аскорбиновая кислота', 300),
        ('Продукт 4', 'Рыбий жир', 400)
    ]

    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.executemany("""INSERT INTO Products (title, description, price) VALUES (?, ?, ?)""", items)
        db.commit()
