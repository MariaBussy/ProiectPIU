from peewee import (
    Model, IntegerField, CharField, BooleanField, ForeignKeyField,
    CompositeKey, SqliteDatabase
)

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Book(BaseModel):
    id = IntegerField(primary_key=True)
    nume = CharField(max_length=255, null=False)
    nr_pagini = IntegerField(null=False)
    gen = CharField(max_length=255, null=False)
    editura = CharField(max_length=255, null=False)
    descriere = CharField(max_length=4000, null=False)
    cale_fisier = CharField(max_length=255)
    cale_poza = CharField(max_length=255)
    is_disabled = BooleanField(null=False)

    class Meta:
        db_table = "carti"
    
class Author(BaseModel):
    id = IntegerField(primary_key=True)
    nume = CharField(max_length=255, null=False)
    descriere = CharField(max_length=4000)
    
    class Meta:
        db_table = "autori"

class Book_Author(BaseModel):
    id_carte = ForeignKeyField(
        Book,
        backref='carti',
        on_delete='CASCADE',
        column_name='id_carte'
    )

    id_autor = ForeignKeyField(
        Author,
        backref='autori',
        on_delete='CASCADE',
        column_name='id_autor'
    )

    class Meta:
        primary_key = CompositeKey('id_carte', 'id_autor')
        db_table = "carte_autor"


class Bookmark(BaseModel):
    id_carte = ForeignKeyField(
        Book,
        backref='carti',
        on_delete='CASCADE',
        column_name='id_carte'
    )

    pagina_default = IntegerField()
    pagina_user = IntegerField()

    class Meta:
        db_table = "bookmarks"

db.connect()
db.create_tables([Book, Author, Book_Author, Bookmark])