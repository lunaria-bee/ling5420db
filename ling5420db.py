#!/usr/bin/env python3

from peewee import *


_db = SqliteDatabase('ling5420db.sqlite')


class BaseModel(Model):
    '''TODO'''

    class Meta:
        database = _db


# Data Tables #
class Language(BaseModel):
    '''TODO'''

    name = CharField()
    '''TODO'''


class Note(BaseModel):
    '''TODO'''

    text = TextField()
    '''TODO'''

    language = ForeignkeyField(Language, backref='notes')
    '''TODO'''


class Tag(BaseModel):
    '''TODO'''

    text = TextField()
    '''TODO'''


class Example(BaseModel):
    '''TODO'''

    text = TextField()
    '''TODO'''

    gloss = TextField()
    '''TODO'''

    translation = TextField()
    '''TODO'''


# Relation Tables #
class TagRelation(BaseModel):
    '''TODO'''

    tag = ForeignKey(Tag, backref='note_links')
    '''TODO'''

    note = ForeignKey(Note, backref='tag_links')


class ExampleRelation(BaseModel):
    '''TODO'''

    example = ForeignKey(Example, backref='note_links')
    '''TODO'''

    note = ForeignKey(Note, backref='example_links')
    '''TODO'''
