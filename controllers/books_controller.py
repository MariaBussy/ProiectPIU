
from database.models import Book
from playhouse.shortcuts import model_to_dict



"""
SELECT * FROM books;
"""
def get_books() -> list:
    books = Book.select()
    if books is None:
        return None
    return [model_to_dict(book) for book in books]

"""
SELECT * FROM books b WHERE b.id = id;
"""
def get_book(id: int) -> dict | None:
    if id is not None and id <= 0:
        return None
    
    book = Book.select().where(Book.id == id).first()
    if book is None:
        return None
    return model_to_dict(book)