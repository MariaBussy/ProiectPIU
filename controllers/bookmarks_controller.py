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
    
    bookmarks = Bookmark.select().where(Bookmark.id_carte == book_id)
    return [model_to_dict(bookmark) for bookmark in bookmarks]

def get_last_page_bookmark(book_id: int):
    
    last_read_bookmark = Bookmark.select().where(Bookmark.id_carte == book_id).first()
    
    if last_read_bookmark:
        return model_to_dict(last_read_bookmark)
    else:
        print("No bookmark found for the provided book_id")
        return None  

def update_last_bookmark_default_page(book_id: int, current_page: int):
    try:
        last_read_bookmark = Bookmark.select().where(Bookmark.id_carte == book_id).first()

        if last_read_bookmark:
            last_read_bookmark.pagina_default = current_page
            last_read_bookmark.pagina_user = current_page + 1
            last_read_bookmark.save()

            last_read_bookmark = Bookmark.select().where(Bookmark.id_carte == book_id).first()
            print(f"Updated last page with: {last_read_bookmark.pagina_default}")
        last_bookmark = (Bookmark
                         .select()
                         .where(Bookmark.id_carte == book_id)
                         .order_by(Bookmark.id.desc())
                         .first())

        if last_bookmark:
            last_bookmark.pagina_default = current_page
            last_bookmark.save()
    except Exception as e:
        print("[Error updating 'Last Read Page' bookmark]", e)

