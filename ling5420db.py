#!/usr/bin/env python3

import ling5420db_model as db

import argparse, shutil, sys, textwrap
from functools import partial


parser = argparse.ArgumentParser(
    description='''
    Query a database of LING 5420 notes and examples.
    ''',
)
parser.add_argument(
    '-l', '--language',
    help='''
    Select notes by language. May be used alone or in conjunction with --tags.
    ''',
)
parser.add_argument(
    '-t', '--tags',
    action='extend',
    nargs='+',
    default=[],
    type=str,
    help='''
    Select notes by tag(s). May be used alone or in conjunction with --language.
    ''',
)
parser.add_argument(
    '-T', '--hide-tags',
    action='store_true',
    help='''
    Do not show tags for selected notes.
    ''',
)
parser.add_argument(
    '-E', '--hide-examples',
    action='store_true',
    help='''
    Do not show examples for selected notes.
    ''',
)
parser.add_argument(
    '-m', '--max-examples',
    type=int,
    help='''
    Maximum number of examples to show for each note. Does nothing if --hide-examples is
    set.
    ''',
)
parser.add_argument(
    '-H', '--disable-error-helper',
    action='store_true',
    help='''
    Do not try to identify user errors in the event of a failed query.
    ''',
)


def align_paired_strings(width, word_list_1, word_list_2):
    '''Construct new strings to align strings from a pair of lists.

    word_list_1 and word_list_2 *must* have the same length.

    Parameters
    width: Maximum width of each line.
    word_list_1: List of strings to align.
    word_list_2: List of strings to align.

    Return: List of pairs of strings. Each pair is itself structured as a list, where the
            first element is a row of the string constructed from word_list_1, and the
            second element is a row of the string constructed from word_list_2.

    '''
    if len(word_list_1) != len(word_list_2):
        raise ueError(f"Arguments s1 and s2 have non-matching word counts "
                         + f"({len(word_list_1)} and {len(word_list_2)} respectively).)")

    remaining_available_width = width
    paired_rows = [["", ""]]
    for w1, w2 in zip(word_list_1, word_list_2):

        width_to_fill = max(len(w1), len(w2)) + 2

        if remaining_available_width < width_to_fill:
            paired_rows.append(("", ""))
            remaining_available_width = width

        paired_rows[-1][0] += f"{w1:{width_to_fill}}"
        paired_rows[-1][1] += f"{w2:{width_to_fill}}"
        remaining_available_width -= width_to_fill

    return paired_rows


def query_and_print(
        language=None,
        tags=[],
        hide_tags=False,
        hide_examples=False,
        max_examples=None,
        disable_error_helper=False,
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

    for t in tags: # TODO there has got to be a better way to do this
        note_query = (
            note_query
            .intersect(
                db.Note
                .select()
                .join(db.TagRelation)
                .join(db.Tag)
                .where(db.Tag.name == t)
            )
        )

    # Print results
    terminal_width = shutil.get_terminal_size().columns
    std_fill = partial(
        textwrap.fill,
        initial_indent="  ",
        subsequent_indent="  ",
        width=terminal_width-2,
    )

    for note in note_query:
        print()
        print(f"Note {note.id}: {note.language.name}", end="")

        # Print tags (if applicable)
        if not hide_tags:
            tag_query = (
                db.Tag
                .select()
                .join(db.TagRelation)
                .join(db.Note)
                .where(db.Note.id == note.id)
                .order_by(db.Tag.name)
            )
            if tag_query:
                tag_str = " (" + ", ".join(t.name for t in tag_query) + ")"
                header_len = len(f"Note {note.id}: {note.language.name}")
                print(
                    textwrap.fill(
                        tag_str,
                        subsequent_indent=" "*header_len,
                        width=terminal_width-2,
                    )
                )
        else:
            print()

        # Print note
        print()
        print(std_fill(note.text))

        # Print examples (if applicable)
        if not hide_examples:
            example_query = (
                db.Example
                .select()
                .join(db.Note)
                .where(db.Note.id == note.id)
            )

            if not max_examples is None:
                example_query = example_query.limit(max_examples)

            for e in example_query:

                newline_before_translation = False

                # Print original and/or gloss
                if e.original and e.gloss:
                    aligned_pairs = align_paired_strings(
                        terminal_width - 4,
                        e.original.split(),
                        e.gloss.split(),
                    )
                    for row_pair in aligned_pairs:
                        print()
                        print(" ", row_pair[0])
                        print(" ", row_pair[1])
                    if len(aligned_pairs) > 1:
                        newline_before_translation = True

                elif e.original:
                    print()
                    print(std_fill(" ".join(e.original.split())))

                elif e.gloss:
                    print()
                    print(std_fill(" ".join(e.gloss.split())))

                # Print translation
                if e.translation:
                    if newline_before_translation: print()
                    print(std_fill(e.translation))


    # Error helper for empty queries
    if len(note_query) == 0 and not disable_error_helper:
        if not language is None:
            if db.Language.get_or_none(name=language) is None:
                print(f"\nLanguage '{language}' not found in database.")

            elif not db.Note.select().join(db.Language).where(db.Language.name==language):
                print(f"\nNo notes associated with {language} in database.")

        elif (not tags == []) and all(db.Tag.get_or_none(name=t) is None for t in tags):
            taglist = ', '.join("'" + t + "'" for t in tags)
            print(f"\nNo such tag(s) {taglist} in database.")

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


if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])

    db.open_()
    query_and_print(**vars(args))
    db.close()
