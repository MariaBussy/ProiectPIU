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
    # book = {
    #     "id": 7,
    #     "nume": "Harry Potter",
    #     "nr_pagini": 100,
    #     "gen": "Drama",
    #     "editura": "Editura",
    #     "descriere": "Ana are mere",
    #     "cale_fisier": "sjhbsajasd",
    #     "cale_poza": "C:/Users/EU/Desktop/New folder (2)/ProiectPIU/Photos/Harry.jpeg",
    #     "is_disabled": 0
    # }
    # insert_book(book)
    app = create_app()
    sys.exit(app.exec_())

