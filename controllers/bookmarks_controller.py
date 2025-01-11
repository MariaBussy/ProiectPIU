from database.models import Bookmark
from playhouse.shortcuts import model_to_dict

"""
SELECT * FROM bookmarks b WHERE b.id = id;
"""
def get_bookmark(id: int) -> dict:
    if id is not None and id <= 0:
        return None
    
    bookmark = Bookmark.select().where(Bookmark.id == id).first()
    if bookmark is None:
        return None
    
    return model_to_dict(bookmark)

"""
Inserts a bookmark in db.
"""
def insert_bookmark(bookmark: dict):
    try:
        inserted_bookmark = Bookmark.create(**bookmark)
        return model_to_dict(inserted_bookmark)
    except Exception as e:
        print("[Error]", e)
        return None

"""
Deletes a bookmark from db.
"""
def delete_bookmark(id: int):
    if not Bookmark.select().where(Bookmark.id == id).exists():
        return "Nu exista aceast autor."

    return Bookmark.delete().where(Bookmark.id == id).execute()

def get_bookmarks_for_book(book_id: int) -> list:
    if book_id is not None and book_id <= 0:
        return []
    
    # Selectează toate marcajele pentru cartea respectivă
    bookmarks = Bookmark.select().where(Bookmark.id_carte == book_id)
    return [model_to_dict(bookmark) for bookmark in bookmarks]
