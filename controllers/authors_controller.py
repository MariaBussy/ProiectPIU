from database.models import Author, Book_Author
from playhouse.shortcuts import model_to_dict

"""
SELECT * FROM authors;
"""
def get_authors() -> list:
    authors = Author.select()
    if authors is None:
        return None
    return [model_to_dict(author) for author in authors]

"""
SELECT * FROM authors a WHERE a.id = id;
"""
def get_author(id: int) -> dict:
    if id is not None and id <= 0:
        return None
    
    author = Author.select().where(Author.id == id).first()
    if author is None:
        return None
    return model_to_dict(author)

"""
Inserts an author in db.
"""
def insert_author(author: dict):
    try:
        # Creează autorul folosind modelul Author
        inserted_author = Author.create(**author)
        
        # Returnează un dicționar cu datele autorului
        return model_to_dict(inserted_author)
    except Exception as e:
        print("[Error]", e)
        return None

"""
Deletes an author from d.
"""
def delete_author(id: int):
    if not Author.select().where(Author.id == id).exists():
        return "Nu exista aceast autor."

    return Author.delete().where(Author.id == id).execute()

def get_author_by_name(author_name: str) -> dict | None:
    try:
        author = Author.select().where(Author.nume == author_name).first()
        if author:
            return model_to_dict(author)
        return None
    except Exception as e:
        print("[Error]", e)
        return None
    
def insert_book_author(book_id: int, author_id: int):
    try:
        Book_Author.create(id_carte=book_id, id_autor=author_id)
    except Exception as e:
        print("[Error]", e)
