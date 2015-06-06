"""
    Mailthon Docs Extensions
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Style taken from Armin Ronacher's awesome Jinja2 style.

    :copyright: (c) 2015 Eeo Jun
    :license: MIT
"""

from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Operator, Generic, Text


class JinjaStyle(Style):
    title = 'Jinja Style'
    default_style = ""
    styles = {
        Comment:                    'italic #aaaaaa',
        Comment.Preproc:            'noitalic #B11414',
        Comment.Special:            'italic #505050',

        Keyword:                    'bold #B80000',
        Keyword.Type:               '#808080',

        Operator.Word:              'bold #B80000',

        Name.Builtin:               '#333333',
        Name.Function:              '#333333',
        Name.Class:                 'bold #333333',
        Name.Namespace:             'bold #333333',
        Name.Entity:                'bold #363636',
        Name.Attribute:             '#686868',
        Name.Tag:                   'bold #686868',
        Name.Decorator:             '#686868',

        String:                     '#AA891C',
        Number:                     '#444444',

        Generic.Heading:            'bold #000080',
        Generic.Subheading:         'bold #800080',
        Generic.Deleted:            '#aa0000',
        Generic.Inserted:           '#00aa00',
        Generic.Error:              '#aa0000',
        Generic.Emph:               'italic',
        Generic.Strong:             'bold',
        Generic.Prompt:             '#555555',
        Generic.Output:             '#888888',
        Generic.Traceback:          '#aa0000',

        Error:                      '#F00 bg:#FAA'
    }


def setup(sphinx):
    pass
