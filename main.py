import sys
from database.models import Book
from controllers.authors_controller import *
from controllers.books_controller import *
from controllers.bookmarks_controller import *
from controllers.epub_controller import *
from interface.ui_app import create_app
import sys

if __name__ == "__main__":
    app = create_app()
    sys.exit(app.exec_())

