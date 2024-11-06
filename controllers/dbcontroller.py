
from database.models import (Book, Author, Bookmark)
from playhouse.shortcuts import model_to_dict

"""
SELECT * FROM books;
"""
def get_books() -> list:
    books = Book.select()
    return [model_to_dict(books) for book in books]


"""
SELECT * FROM books b WHERE b.id = id;
"""
def get_book(id: int) -> dict | None:
    if id is not None and id <= 0:
        return None
    
    book = Book.select().where(Book.id == id).first()
    return model_to_dict(book)

"""
SELECT * FROM authors;
"""
def get_authors() -> list:
    authors = Author.select()
    return [model_to_dict(author) for author in authors]

"""
SELECT * FROM authors a WHERE a.id = id;
"""
def get_author(id: int) -> dict:
    if id is not None and id <= 0:
        return None
    
    author = Author.select().where(Author.id == id).first()
    return model_to_dict(author)

"""
SELECT * FROM bookmarks b WHERE b.id = id;
"""
def get_bookmark(id: int) -> dict:
    if id is not None and id <= 0:
        return None
    
    bookmark = Bookmark.select().where(Bookmark.id == id).first()
    return model_to_dict(bookmark)

