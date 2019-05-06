from functools import wraps
from os.path import dirname, join

from textx import LanguageDesc
from textx import generator as _generator
from textx import metamodel_from_file

from .generators import TextmateGen

TX_LANG_COLORING_NAME = 'txcl'
TX_LANG_COLORING_METAMODEL = metamodel_from_file(join(dirname(__file__),
                                                      'grammars/coloring.tx'))


STRINGS = []


def str_obj_processor(str_match):
    global STRINGS
    STRINGS.append(str_match.match)


TX_LANG_TEXTX_METAMODEL = metamodel_from_file(join(dirname(__file__),
                                                   'grammars/textx.tx'))
TX_LANG_TEXTX_METAMODEL.register_obj_processors(
    {'StrMatch': str_obj_processor})


coloring_lang = LanguageDesc(
    name=TX_LANG_COLORING_NAME,
    pattern='*.txcl',
    description='A language for syntax highlight definition.',
    metamodel=TX_LANG_COLORING_METAMODEL)


def _parse_coloring_file(coloring_file):
    return TX_LANG_COLORING_METAMODEL.model_from_file(coloring_file)


def _parse_grammar_file(grammar_file):
    global STRINGS
    STRINGS.clear()
    return TX_LANG_TEXTX_METAMODEL.model_from_file(grammar_file)


def generator(language, target):
    def decorator(f):
        @_generator(language, target)
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Parse grammar with textX metamodel
            grammar_file = args[1].file_name
            tx_model = _parse_grammar_file(grammar_file)

            # Parse coloring model if provided
            cl_file = kwargs.get('cl')
            coloring_model = _parse_coloring_file(cl_file) if cl_file else None

            f(tx_model, coloring_model, *args[2:])
        return wrapper
    return decorator


@generator('textX', 'textmate')
def textmate_gen(grammar_model, coloring_model, output_path, overwrite, debug=False):
    """Generating textmate syntax highlighting from textX grammars"""
    TextmateGen.generate(STRINGS)
