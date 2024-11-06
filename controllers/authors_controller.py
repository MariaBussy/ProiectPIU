
from database.models import Author
from playhouse.shortcuts import model_to_dict

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
