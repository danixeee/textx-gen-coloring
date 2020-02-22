import re
import string
from textx import metamodel_for_language, get_children_of_type

from .metamodels import coloring_mm
from .templates import jinja_env

ASCII_LETTERS = string.ascii_letters


class GrammarInfo:
    """
    Holds grammar information needed to generate syntax highlighting file(s).
    """

    def __init__(self, name):
        self.name = name
        self.keywords = []
        self.regexes = []
        self.comments = []


class _TextmateGen:
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


def _escape_keyword(keyword):
    """
    Prepend `\\\\` to all chars that are not ascii letters.
    NOTE: `re.escape` does not work the same for 3.6 and 3.7 versions.
    """
    return "".join(
        [
            letter if letter in ASCII_LETTERS else "\\\\{}".format(letter)
            for letter in keyword
        ]
    )


def _get_textx_rule_name(parent_rule):
    """
    Iterate parent instances until `TextxRule` instance.
    """
    while not type(parent_rule).__name__ == "TextxRule":
        parent_rule = parent_rule.parent
    return parent_rule.name


def _parse_syntax_spec(syntax_spec):
    """
    Parse syntax specification with coloring metamodel.
    """
    return coloring_mm.model_from_file(syntax_spec)


def _parse_grammar(grammar_file, lang_name, skip_keywords=False):
    """
    Collects information about grammar using textX object processors.
    Currently collects only `StrMatch` and `ReMatch` rules, since those are
    language keywords and identifiers.
    """
    textx_mm = metamodel_for_language("textx")
    grammar_model = textx_mm.grammar_model_from_file(grammar_file)
    grammar_info = GrammarInfo(lang_name)

    for str_match in get_children_of_type("StrMatch", grammar_model):
        keyword = _escape_keyword(str_match.match)
        if keyword not in grammar_info.keywords:
            grammar_info.keywords.append(keyword)

    for reg_match in get_children_of_type("ReMatch", grammar_model):
        if _get_textx_rule_name(reg_match.parent) == "Comment":
            grammar_info.comments.append(reg_match.match)
        else:
            grammar_info.regexes.append(reg_match.match)

    return grammar_info


def generate_textmate_syntax(model, lang_name, syntax_spec=None, skip_keywords=False):
    """
    Gets textmate generator depending on provided arguments.
    If syntax specification file is not provided, default generator is used
    to create textmate syntax file.
    """
    grammar_file = model().file_name if callable(model) else model.file_name
    syntax_model = _parse_syntax_spec(syntax_spec) if syntax_spec else None

    grammar_info = _parse_grammar(grammar_file, lang_name, skip_keywords)

    if syntax_model:
        raise NotImplementedError("Not supported yet!")
    else:
        return _TextmateDefaultGen(grammar_info).generate()
