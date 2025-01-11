from peewee import SqliteDatabase
from models import Book, Author, Book_Author, Bookmark

db = SqliteDatabase('database.db')

def clear_database():
    try:
        with db.atomic():
            Bookmark.delete().execute()  
            Book_Author.delete().execute()  
            
            Book.delete().execute() 
            Author.delete().execute() 
        
        print("Baza de date a fost golita cu succes.")
    
    except Exception as e:
        print(f"A aparut o eroare: {e}")

if __name__ == "__main__":
    clear_database()
