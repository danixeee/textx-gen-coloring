import re
from collections.abc import ABC
from functools import partial

from .metamodels import coloring_mm, textx_mm
from .templates import jinja_env, textmate_template_dir


class GrammarInfo:
    """
    Holds grammar information needed to generate syntax highlighting file(s).
    """

    def __init__(self, name):
        self.name = name
        self.keywords = []


class _TextmateGen(ABC):
    """
    Abstract textmate generator.
    """

    _template = jinja_env.get_template("textmate/language.json.template")

    def __init__(self, grammar_info):
        self.grammar_info = grammar_info

    def _get_comment(self):  # pragma: no cover
        return {}

    def _get_keywords(self):  # pragma: no cover
        return []

    def _get_operations(self):  # pragma: no cover
        return []

    def _get_regular_expressions(self):  # pragma: no cover
        return []

    def generate(self):
        return self._template.render(
            {
                "name": self.grammar_info.name,
                "comment": self._get_comment(),
                "keywords": self._get_keywords(),
                "operations": self._get_operations(),
                "regular_expressions": self._get_regular_expressions(),
            }
        )


class _TextmateDefaultGen(_TextmateGen):
    """
    Generator which creates default textmate syntax coloring file. It uses only
    information from grammar.
    """

    def __init__(self, grammar_info):
        super().__init__(grammar_info)

    def _get_comment(self):
        return {"line": "//", "block_start": r"/\\*", "block_end": r"\\*/"}

    def _get_keywords(self):
        def _kwd_class(kwd):
            if re.match("^[a-zA-Z0-9_]*$", kwd):
                return "support.class"
            else:
                return "constant.language"

        return [
            {"match": kwd, "name": _kwd_class(kwd)}
            for kwd in self.grammar_info.keywords
        ]


def _parse_syntax_spec(syntax_spec):
    """
    Parse syntax specification with coloring metamodel.
    """
    return coloring_mm.model_from_file(syntax_spec)


def _parse_grammar(grammar_file, lang_name):
    """
    Collects information about grammar using textX object processors. Currently
    collects only `StrMatch` rules, since those are language keywords.
    """
    textx_mm.obj_processors = {}
    grammar_info = GrammarInfo(lang_name)

    # Object processors
    def _str_obj_processor(grammar_info, str_match):
        """Get language keywords (all strings in language grammar definition"""
        grammar_info.keywords.append(str_match.match)

    textx_mm.register_obj_processors(
        {"StrMatch": partial(_str_obj_processor, grammar_info)}
    )

    textx_mm.model_from_file(grammar_file)

    return grammar_info


def generate_textmate_syntax(model, lang_name, syntax_spec=None):
    """
    Gets textmate generator depending on provided arguments.
    If syntax specification file is not provided, default generator is used
    to create textmate syntax file.
    """
    grammar_file = model().file_name if callable(model) else model.file_name
    syntax_model = _parse_syntax_spec(syntax_spec) if syntax_spec else None

    grammar_info = _parse_grammar(grammar_file, lang_name)

    if syntax_model:
        raise NotImplementedError("Not supported yet!")
    else:
        return _TextmateDefaultGen(grammar_info).generate()
