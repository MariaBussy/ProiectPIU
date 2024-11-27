from database.models import Book
from controllers.authors_controller import *
from controllers.books_controller import *
from controllers.bookmarks_controller import *
from controllers.epub_controller import *

if __name__ == "__main__":
    file = "blanchard-a-dear-little-girl.epub"
    print(process_epub(file))