import sqlite3

DB_NAME = 'products.db'


def initiate_db():
    """Создаем таблицу Products"""
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS Products(
                            id INTEGER PRIMARY KEY, 
                            title TEXT NOT NULL,
                            description TEXT,
                            price INTEGER NOT NULL)"""
                       )
        db.commit()


def get_all_products():
    """Возвращаем все записи из таблицы Products"""
    with sqlite3.connect(DB_NAME) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM Products""")
        return cursor.fetchall()


if __name__ == '__main__':
    exit()
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
