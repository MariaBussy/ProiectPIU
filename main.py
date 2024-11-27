from database.models import Book
from controllers.authors_controller import *
from controllers.books_controller import *
from controllers.bookmarks_controller import *

if __name__ == "__main__":
    print("Autori: ", get_authors())
    print("Carti: ", get_books())