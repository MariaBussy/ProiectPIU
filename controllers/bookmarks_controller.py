
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
        inserted_bookmark = inserted_bookmark.create(**bookmark)
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