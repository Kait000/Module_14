import sqlite3

db = sqlite3.connect('not_telegram.db')  # устанавливаем соединение с БД
cursor = db.cursor()

"""Создаем таблицу Users"""
query = """CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY, 
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)"""
cursor.execute(query)
db.commit()

"""Составляем список кортежей для добавления в таблицу"""
data = []
for i in range(1, 11):
    data.append((f'User{i}', f'example{i}@gmail.com', i*10, 1000))
"""Добавляем записи в таблицу"""
cursor.executemany("""INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)""", data)
db.commit()

"""Составляем свой список id таблицы Users, т.к. в рабочих БД индексы могут идти не попорядку"""
data_id = []    # содержит список id всех записей
query = """SELECT id FROM Users ORDER BY id"""
for i in cursor.execute(query):
    data_id.append(i[0])

"""Для каждой второй записи меняем balance на 500"""
for i in range(0, len(data_id), 2):
    cursor.execute("""UPDATE Users SET balance = ? WHERE id = ?""", (500, i+1))
db.commit()

"""Удаляем каждую третью запись"""
for i in range(0, len(data_id), 3):
    cursor.execute("""DELETE FROM Users WHERE id = ?""", (i+1,))
db.commit()

"""Делаем выборку всех записей где возраст != 60"""
cursor.execute("""SELECT * FROM Users WHERE age != ?""", (60,))
for i in cursor.fetchall():
    print(f'Имя: {i[1]} | Почта: {i[2]} | Возраст: {i[3]} | Баланс: {i[4]}')

db.close()


"""Новый код для домашнего задания module_14_2"""
with sqlite3.connect('not_telegram.db') as db:
    cursor = db.cursor()

    """Удаляем из таблицы запись с id = 6"""
    cursor.execute("""DELETE FROM Users WHERE id = ?""", (6,))
    db.commit()

    """Подсчет кол-ва строк"""
    cursor.execute("""SELECT COUNT(*) FROM Users""")
    total_users = cursor.fetchone()[0]

    """Сумма баланса всех ползователей"""
    cursor.execute("""SELECT SUM(balance) FROM Users""")
    all_balances = cursor.fetchone()[0]

    """Средний баланс всех пользователей"""
    print()
    print(all_balances / total_users)
