from functools import partial, wraps
from os.path import dirname, join

import click
from textx import LanguageDesc
from textx import generator as _generator
from textx import metamodel_from_file

from .generators import LanguageData, get_textmate_generator
from .metamodels import coloring_mm, textx_mm

TEXTMATE_LANG_TARGET = ('textX', 'textmate')
COLORING_LANG_NAME = 'txcl'


coloring_lang = LanguageDesc(
    name=COLORING_LANG_NAME,
    pattern='*.txcl',
    description='A language for syntax highlight definition.',
    metamodel=coloring_mm)


def _parse_coloring_file(coloring_file):
    return coloring_mm.model_from_file(coloring_file)


def _get_language_data(grammar_file, lang_name):
    lang_data = LanguageData(lang_name)

    # Object processors
    def _str_obj_processor(lang_data, str_match):
        """Get language keywords (all strings in language grammar definition"""
        lang_data.keywords.append(str_match.match)

    if not textx_mm.obj_processors:
        textx_mm.register_obj_processors({
            'StrMatch': partial(_str_obj_processor, lang_data)
        })

    # Parse file, but ignore returned model
    textx_mm.model_from_file(grammar_file)

    return lang_data


def generator(language, target):
    def decorator(f):
        @_generator(language, target)
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get language name
            lang_name = kwargs.get('lang-name')
            if not lang_name:
                raise Exception('Language name is required (--lang-name XYZ).')

            # Parse grammar with textX metamodel
            grammar_file = args[1].file_name
            lang_data = _get_language_data(grammar_file, lang_name)

            # Parse coloring model if provided
            cl_file = kwargs.get('cl')
            coloring_model = _parse_coloring_file(cl_file) if cl_file else None

            f(lang_data, coloring_model, *args[2:])
        return wrapper
    return decorator


@generator(*TEXTMATE_LANG_TARGET)
def textmate_gen(lang_data, coloring_model, output_path='', overwrite=True, debug=False):  # noqa
    """Generating textmate syntax highlighting from textX grammars"""
    # TODO: Do not ignore `overwrite` and `debug` fields...

    generator = get_textmate_generator(lang_data, coloring_model)
    textmate_json = generator.generate()

    if not output_path:
        click.echo(textmate_json)
        return textmate_json

    with open(output_path, 'w') as f:
        f.write(textmate_json)
