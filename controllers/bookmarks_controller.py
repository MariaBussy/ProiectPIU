
from database.models import Bookmark
from playhouse.shortcuts import model_to_dict

"""
SELECT * FROM bookmarks b WHERE b.id = id;
"""
def get_bookmark(id: int) -> dict:
    if id is not None and id <= 0:
        return None
    
    bookmark = Bookmark.select().where(Bookmark.id == id).first()
    return model_to_dict(bookmark)

