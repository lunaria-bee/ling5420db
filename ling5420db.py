#!/usr/bin/env python3

import ling5420db_model as db


def query_and_print(
        language=None,
        tags=(),
        show_examples=True,
        examples_per_note=0,
        show_tags=True,
):
    '''Query the database and print the results.'''

    note_query = db.Note.select()

    if not language is None:
        note_query = (
            note_query
            .switch(db.Note)
            .join(db.Language)
            .where(db.Language.name == language)
        )

    for t in tags:
        note_query = (
            note_query
            .switch(db.Note)
            .join(db.TagRelation)
            .join(db.Tag)
            .where(db.Tag.name == t)
        )

    for note in note_query:
        print()
        print(f"Note {note.id}: {note.language.name}", end="")

        if show_tags:
            tag_query = (
                db.Tag
                .select()
                .join(db.TagRelation)
                .join(db.Note)
                .where(db.Note.id == note.id)
                .order_by(db.Tag.name)
            )
            print(" (" + ", ".join(t.name for t in tag_query) + ")")
        else:
            print()

        print()
        print(" ", note.text)

        if show_examples:
            example_query = (
                db.Example
                .select()
                .join(db.Note)
                .where(db.Note.id == note.id)
            )

            if examples_per_note > 0:
                example_query = example_query.limit(examples_per_note)

            for e in example_query:
                print()
                print(" ", '\t'.join(e.original.split()))
                print(" ", '\t'.join(e.gloss.split()))
                print(" ", e.translation)

    print()


def interactive_add_note():
    '''Interactively add a note, with tags and examples.'''

    # Get note language
    is_language_valid = False
    while not is_language_valid:
        language_name = input("Language: ")
        language = db.Language.get_or_none(name=language_name)
        if language is None:
            print(f"No such language \"{language_name}\".")
            add = bool(input("Add to database? (y/n): ").lower() == 'y')
            if add:
                language = db.Language.create(name=language_name)
                language.save()
                is_language_valid = True
            else:
                print(f"Valid languages are: {', '.join(lang.name for lang in db.Language.select())}")
        else:
            is_language_valid = True

    # Get note text
    text = input("Note text: ")

    # Create note db entry
    note = db.Note.create(text=text, language=language)
    note.save()

    # Add examples
    add_example = bool(input("Add an example? (y/n): ").lower() == 'y')
    while add_example:
        example_original = " ".join(input("Original: ").split())
        example_gloss = " ".join(input("Gloss: ").split())
        example_translation = input("Translation: ")
        db.Example(
            original=example_original,
            gloss=example_gloss,
            translation=example_translation,
            note=note,
        ).save()

        add_example = bool(input("Add another exaxmple? (y/n): ").lower() == 'y')

    # Create tag relations
    last_tag = False
    while not last_tag:
        tag_name = input("Tag: ")
        if tag_name:
            tag, _ = db.Tag.get_or_create(name=tag_name)
            db.TagRelation(tag=tag, note=note).save()
        else:
            last_tag = True


def interactive_add_multiple_notes():
    '''Interactively add an arbitrary number of notes.'''
    add_another_note = True
    while add_another_note:
        interactive_add_note()
        print()
        add_another_note = bool(input("Add another note? (y/n): ").lower() == 'y')
