import epub_metadata

"""
processes a epub file and returns a dict with Book data.
"""
def process_epub(
            file_path: str, 
            genre: str | None = None, 
            file_image_path: str | None = None
            ) -> list:
    
    if file_path is None:
        raise Exception("File path is None.")

    if genre is None:
        genre = "No genre."

    if file_image_path is None:
        file_image_path = "default.jpg"

    epub_data = epub_metadata.epub(file_path)
    metadata = epub_data.metadata

    name = metadata.title if metadata.title else "Unknown Title"
    author = metadata.creator if metadata.creator else "Unknown Author"
    publisher = metadata.publisher if metadata.publisher else "Unknown Publisher"
    description = metadata.description if metadata.description else "No Description Available"

    book = {
        "nume": name,
        "nr_pagini": 0,
        "gen": genre,
        "editura": publisher,
        "descriere": description,
        "cale_fisier": file_path,
        "cale_poza": file_image_path,
        "is_disabled": False
    }

    author = {
        "nume": author,
        "descriere": ""
    }

    return (book, author)