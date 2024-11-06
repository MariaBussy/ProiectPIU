
from database.models import *
from playhouse.shortcuts import model_to_dict
import sys

from controllers.dbcontroller import *

if __name__ == "__main__":
    print(get_books())