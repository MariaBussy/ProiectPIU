import sys
from database.models import Book
from controllers.authors_controller import *
from controllers.books_controller import *
from controllers.bookmarks_controller import *
from controllers.epub_controller import *
from interface.ui_app import create_app
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

if __name__ == "__main__":
    print("Autori: ", get_authors())
    print("Carti: ", get_books())
    app = create_app()
    sys.exit(app.exec_())

