import re
from abc import ABC, abstractmethod

from .templates import jinja_env, textmate_template_dir


class LanguageData:
    """
    Holds language information needed to generate syntax highlighting file(s).
    """

    def __init__(self, name):
        self.name = name
        self.keywords = []


class _TextmateGen(ABC):
    _template = jinja_env.get_template('textmate/language.json.template')

    def __init__(self, lang_data):
        self.lang_data = lang_data

    def _get_comment(self):
        return {}

    def _get_keywords(self):
        return []

    def _get_operations(self):
        return []

    def _get_regular_expressions(self):
        return []

    def generate(self):
        return self._template.render({
            'name': self.lang_data.name,
            'comment': self._get_comment(),
            'keywords': self._get_keywords(),
            'operations': self._get_operations(),
            'regular_expressions': self._get_regular_expressions()
        })


class _TextmateDefaultGen(_TextmateGen):
    def __init__(self, lang_data):
        super().__init__(lang_data)

    def _get_comment(self):
        return {
            'line': '//',
            'block_start': r'/\\*',
            'block_end': r'\\*/'
        }

    def _get_keywords(self):
        def _kwd_class(kwd):
            if re.match("^[a-zA-Z0-9_]*$", kwd):
                return 'support.class'
            else:
                return 'constant.language'

        return [{
            'match': kwd,
            'name': _kwd_class(kwd)
        } for kwd in self.lang_data.keywords]


def get_textmate_generator(lang_data, coloring_model):
    if coloring_model:
        raise NotImplementedError('Not supported yet!')
    else:
        return _TextmateDefaultGen(lang_data)
