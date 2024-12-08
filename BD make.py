import sqlite3

# Создаем соединение с базой данных
con = sqlite3.connect('books.db')

# Создаем таблицу для хранения информации о книгах
with con:
    con.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        year INTEGER NOT NULL,
        genre TEXT NOT NULL,
        image_url TEXT NOT NULL
    )
    ''')

# Примеры книг
books = [
    ("1984", "Джордж Оруэлл", 1949, "Далёкое будущее",
     "1984.jpeg"),
    ("Убийство в Восточном экспрессе", "Агата Кристи", 1934, "Детектив",
     "die.jpg"),
    ("Гордость и предубеждение", "Джейн Остин", 1813, "Роман",
     "pride.jpg"),
    ("Моби Дик", "Герман Мелвилл", 1851, "Приключения",
     "moby.jpg"),
    ("Убить пересмешника", "Харпер Ли", 1960, "Роман",
     "kill.jpg"),
]

# Вставляем данные в таблицу
with con:
    con.executemany('''
    INSERT INTO books (title, author, year, genre, image_url)
    VALUES (?, ?, ?, ?, ?)
    ''', books)
