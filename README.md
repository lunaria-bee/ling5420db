# ling5420db

Build and query a database of notes and examples from LING 5420.

## Requirements

- [Python 3 (3.4 or higher)](https://www.python.org/downloads/)
- [Peewee (3.14 or higher)](http://docs.peewee-orm.com/en/latest/peewee/installation.html)

## Usage

### As a command-line utility

ling5420db.py can be run as a script from the command line (`./ling5420.py` or `python
ling5420db.py`). When used in this mode, the program may only be used to make selection
queries. See the built-in help (`./ling5420.py -h`) for details.

### Interactively in Python

More functionality is available by running ling5420db.py in Python's iteractive mode
(`python -i ling5420db.py`). A few interactive functions are available:

-  `query_and_print`: Does the same thing as calling the program from the
   command line. Takes the same arguments as the command line mode.
-  `interactive_add_note`: Add a note with examples and tags.
-  `interactive_add_multiple_notes`: Add multiple notes without having to repeatedly call
   `interactive_add_note`.
   
See function parameter lists and docstrings for more usage information.

If you're familiar with basic database concepts, it's fairly easy to [write your own
queries in Peewee](docs.peewee-orm.com/en/latest/peewee/querying.html). Peewee also has
some [additional helpers for interactive
use](http://docs.peewee-orm.com/en/latest/peewee/interactive.html).
