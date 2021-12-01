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
    '''The name of the language.'''


class Note(BaseModel):
    '''Note on a feature of a language.'''

    text = TextField()
    '''Text of the note.'''

    language = ForeignKeyField(Language, backref='notes')
    '''The language .'''


class Tag(BaseModel):
    '''Tag describing a cross-linguistic feature.'''

    name = CharField(unique=True)
    '''Text of the tag.'''


class Example(BaseModel):
    '''Example of a feature in a language.'''

    text = TextField()
    '''Original text of the example utterance.'''

    gloss = TextField()
    '''Gloss of the utterance.'''

    translation = TextField()
    '''Translation of the utterance.'''


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


class ExampleRelation(BaseModel):
    '''Indicates an example for a note.'''

    example = ForeignKeyField(Example, backref='note_links')
    '''Example to relate.'''

    note = ForeignKeyField(Note, backref='example_links')
    '''Note to relate.'''

    class Meta:
        # Require each example-note pair to be unique.
        indexes = ( (('example', 'note'), True), )
