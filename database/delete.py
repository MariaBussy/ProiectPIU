from peewee import SqliteDatabase
from models import Book, Author, Book_Author, Bookmark

# Conectează-te la baza de date
db = SqliteDatabase('database.db')

def clear_database():
    """
    Golește toate tabelele din baza de date.
    """
    try:
        # Începe tranzacția
        with db.atomic():
            # Șterge datele din tabelele cu relații (Book_Author și Bookmark) mai întâi pentru a evita erori de chei străine
            Bookmark.delete().execute()  # Șterge toate bookmark-urile
            Book_Author.delete().execute()  # Șterge toate asocierile Book-Author
            
            # Apoi șterge datele din tabelele Book și Author
            Book.delete().execute()  # Șterge toate cărțile
            Author.delete().execute()  # Șterge toți autorii
        
        print("Baza de date a fost golită cu succes.")
    
    except Exception as e:
        print(f"A apărut o eroare: {e}")

# Apelează funcția pentru a goli baza de date
if __name__ == "__main__":
    clear_database()
