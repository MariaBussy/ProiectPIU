
from database.models import *
from playhouse.shortcuts import model_to_dict

if __name__ == "__main__":
    autori = Author.select()

    for autor in autori:
        print(model_to_dict(autor))

    carti = Book.select()

    for carte in carti:
        print(model_to_dict(carte))

    joins = Book_Author.select()

    for join in joins:
        print(model_to_dict(join, recurse=False))