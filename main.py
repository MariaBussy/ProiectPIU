
from database.models import *
from playhouse.shortcuts import model_to_dict
import sys

from controllers.authors_controller import *
from controllers.books_controller import *
from controllers.bookmarks_controller import *

if __name__ == "__main__":
    print("Carte id 1:")
    print(get_book(1))

    print("Carti: ")
    print(get_books())

    print("Autor id 1: ")
    print(get_author(1))

    print("Autori: ")
    print(get_authors())
