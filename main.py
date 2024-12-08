import sys
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QTableWidgetItem


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.last_book = ""

        self.tableWidget.setColumnCount(4)
        self.searchButton.clicked.connect(self.search_books)

        self.con = sqlite3.connect('books.db')
        self.cur = self.con.cursor()

        self.load_books()

    def load_books(self):
        self.cur.execute("SELECT * FROM books")
        books = self.cur.fetchall()

        self.tableWidget.setRowCount(len(books))
        for row, book in enumerate(books):
            title = book[1]
            item = QTableWidgetItem(title)
            self.tableWidget.setItem(row, 0, item)
            self.tableWidget.cellClicked.connect(self.open_book_info)

            author = book[2]
            item = QTableWidgetItem(author)
            self.tableWidget.setItem(row, 1, item)
            self.tableWidget.cellClicked.connect(self.open_book_info)

            year = str(book[3])
            item = QTableWidgetItem(year)
            self.tableWidget.setItem(row, 2, item)
            self.tableWidget.cellClicked.connect(self.open_book_info)

            genre = book[4]
            item = QTableWidgetItem(genre)
            self.tableWidget.setItem(row, 3, item)
            self.tableWidget.cellClicked.connect(self.open_book_info)

    def search_books(self):
        author = self.authorLineEdit.text()
        title = self.titleLineEdit.text()

        data = []
        sql = "SELECT * FROM books WHERE "
        if title not in ("", "Поиск по названию") and \
                author not in ("", "Поиск по автору"):
            sql += "title LIKE ? AND author LIKE ?"
            data.append(title, author)
        elif author not in ("", "Поиск по автору"):
            sql += "author LIKE ?"
            data.append(author)
        elif title not in ("", "Поиск по названию"):
            sql += "title LIKE ?"
            data.append(title)

        books = self.cur.execute(sql, data).fetchall()
        if books:
            self.display_searched_books(books)

    def display_searched_books(self, books):
        self.tableWidget.setRowCount(len(books))
        for row, book in enumerate(books):
            title = book[1]
            item = QTableWidgetItem(title)
            self.tableWidget.setItem(row, 0, item)

            author = book[2]
            item = QTableWidgetItem(author)
            self.tableWidget.setItem(row, 1, item)

            year = str(book[3])
            item = QTableWidgetItem(year)
            self.tableWidget.setItem(row, 2, item)

            genre = book[4]
            item = QTableWidgetItem(genre)
            self.tableWidget.setItem(row, 3, item)

    def open_book_info(self, row, column):
        title = self.tableWidget.item(row, column).text()
        book = self.cur.execute("SELECT * FROM books WHERE title = ?",
                                (title,)).fetchone()

        if book:
            if book != self.last_book:
                self.last_book = book
                self.dialog = BookInfoWindow(book)
                self.dialog.exec()


class BookInfoWindow(QtWidgets.QDialog):
    def __init__(self, book):
        super().__init__()
        uic.loadUi("book_info.ui", self)

        self.titleLabel.setText(f"Название: {book[0]}")
        self.authorLabel.setText(f"Автор: {book[1]}")
        self.yearLabel.setText(f"Год: {book[2]}")
        self.genreLabel.setText(f"Жанр: {book[3]}")

        image_path = book[5]
        if image_path:
            pixmap = QPixmap(image_path)
            self.imageLabel.setPixmap(pixmap)
        else:
            self.imageLabel.setText("Нет изображения")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
