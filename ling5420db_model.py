from peewee import *


_db = SqliteDatabase('ling5420db.sqlite')


class BaseModel(Model):
    '''Base class for database table models'''

    class Meta:
        database = _db


# Data Tables #

class Language(BaseModel):
    '''Language that was studied in class'''

    name = CharField()
    '''The name of the language'''


class Note(BaseModel):
    '''Note on a feature of a language'''

    text = TextField()
    '''Text of the note'''

    language = ForeignkeyField(Language, backref='notes')
    '''The language '''


class Tag(BaseModel):
    '''Tag describing a cross-linguistic feature'''

    text = TextField()
    '''Text of the tag'''


class Example(BaseModel):
    '''Example of a feature in a language'''

    text = TextField()
    '''Original text of the example utterance'''

    gloss = TextField()
    '''Gloss of the utterance'''

    translation = TextField()
    '''Translation of the utterance'''


# Relation Tables #

class TagRelation(BaseModel):
    '''Indicates a tag on a note'''

    tag = ForeignKey(Tag, backref='note_links')
    '''Tag to relate'''

    note = ForeignKey(Note, backref='tag_links')
    '''Note to relate'''


class ExampleRelation(BaseModel):
    '''Indicates an example for a note'''

    example = ForeignKey(Example, backref='note_links')
    '''Example to relate'''

    note = ForeignKey(Note, backref='example_links')
    '''Note to relate'''
