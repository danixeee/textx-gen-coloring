from functools import wraps
from os.path import dirname, join

from textx import LanguageDesc
from textx import generator as _generator
from textx import metamodel_from_file

TX_LANG_COLORING_NAME = 'txcl'
TX_LANG_COLORING_METAMODEL = metamodel_from_file(join(dirname(__file__),
                                                      'coloring.tx'))


coloring = LanguageDesc(
    name=TX_LANG_COLORING_NAME,
    pattern='*.txcl',
    description='A language for syntax highlight definition.',
    metamodel=TX_LANG_COLORING_METAMODEL)


def get_coloring_model(coloring_file):
    return TX_LANG_COLORING_METAMODEL.model_from_file(coloring_file)


def generator(language, target):
    def decorator(f):
        @_generator(language, target)
        @wraps(f)
        def wrapper(*args, **kwargs):
            print('ARGS: {}'.format(args))
            print('KWARGS: {}'.format(kwargs))

            cl_file = kwargs.get('cl')
            cl_model = get_coloring_model(cl_file) if cl_file else None
            f(cl_model, *args)
        return wrapper
    return decorator
