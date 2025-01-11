import epub_metadata
import tika
from tika import parser

def process_epub(
        file_path: str, 
        genre: str | None = None, 
        file_image_path: str | None = None,
        avg_words_per_page: int = 250
        ) -> tuple:
    
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

    no_words = get_epub_content(file_path)["no_words"]

    book = {
        "nume": name,
        "nr_pagini": int(no_words / avg_words_per_page),
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


def get_epub_content(file_path: str)-> dict:
    if file_path is None:
        raise Exception("File path is None.")
    
    parsed = parser.from_file(file_path)
    content = parsed["content"]

    returned_values = {
        "content": content,
        "no_words": len(content.split())
    }

    return returned_values