
from database.models import Author
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
        inserted_author = inserted_author.create(**author)
        return model_to_dict(author)
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
