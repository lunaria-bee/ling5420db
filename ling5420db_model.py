import os
from peewee import *


DB_PATH = 'ling5420db.sqlite'
_db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    '''Base class for database table models.'''

    class Meta:
        database = _db


# Data Tables #

class Language(BaseModel):
    '''Language that was studied in class.'''

    name = CharField(unique=True)
    '''Name of the language.'''


class Note(BaseModel):
    '''Note on a feature of a language.'''

    text = TextField()
    '''Text of the note.'''

    language = ForeignKeyField(Language, backref='notes')
    '''Language the note describes.'''


class Tag(BaseModel):
    '''Tag describing a cross-linguistic feature.'''

    name = CharField(unique=True)
    '''Text of the tag.'''


class Example(BaseModel):
    '''Example of a feature in a language.'''

    original = TextField()
    '''Original text of the example utterance.

    TODO explain alignment with gloss

    '''

    gloss = TextField()
    '''Gloss of the utterance.

    TODO explain alignment with original

    '''

    translation = TextField()
    '''Translation of the utterance.'''

    note = ForeignKeyField(Note, backref='examples')
    '''Note related to the example.'''


# relation Tables #

class TagRelation(BaseModel):
    '''Indicates a tag on a note.'''

    tag = ForeignKeyField(Tag, backref='note_links')
    '''Tag to relate.'''

    note = ForeignKeyField(Note, backref='tag_links')
    '''Note to relate.'''

    class Meta:
        # Require each tag-note pair to be unique.
        indexes = ( (('tag', 'note'), True), )


# Initialization #

def _init():
    '''Initialize the database.'''
    _db.create_tables([Language, Note, Tag, Example, TagRelation])

    Language(name="English").save()
    Language(name="French").save()
    Language(name="Hawai'ian").save()
    Language(name="Southern Sierra Miwok").save()
    Language(name="Coast Miwok").save()


def open_():
    '''Open a connection to the database.'''
    is_initialized = os.path.isfile(DB_PATH)
    _db.connect()
    if not is_initialized: _init()


def close():
    '''Close the database connection.'''
    _db.close()
