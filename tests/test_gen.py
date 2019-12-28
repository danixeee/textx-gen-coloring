import json
import re

import pytest
from click.testing import CliRunner
from textx.cli import textx


def _textmate_gen_cli(grammar_path, **kwargs):
    """Helper function to call the generator.
    kwargs is a dict in format flag: value
    - if flag is passed with one underscore, it will be converted to dash
    - if flag is passed with two underscores, it will be converted to single underscore
    """
    cmd = ["generate", "--target", "textmate", grammar_path]
    for flag, value in kwargs.items():
        flag = (
            flag.replace("__", "_") if flag.find("__") != -1 else flag.replace("_", "-")
        )
        cmd.extend(["--{}".format(flag), value])

    runner = CliRunner()
    result = runner.invoke(textx, cmd)

    try:
        return json.loads(result.stdout.split("\n", 2)[2]), result.exception
    except json.JSONDecodeError:
        return result.stdout, result.exception


def _get_keywords_from_textmate(textmate):
    """Return keywords from textmate object.
    """
    return [
        kw["match"] for kw in textmate["repository"]["language_keyword"]["patterns"]
    ]


def test_textmate_gen_cli_console(lang):
    """Test generating textmate syntax file with default generator and output the result
    to the console.

    Command:
        textX generate --target textmate ./examples/workflow/workflow.tx --name Workflow
    """
    name = lang["name"]
    keywords = lang["keywords"]
    grammar_path = lang["grammar_path"]

    output, _ = _textmate_gen_cli(grammar_path, name=name)
    output_kws = _get_keywords_from_textmate(output)
    for kw in keywords:
        assert kw in output_kws


def test_textmate_gen_cli_console_bad_args(lang):
    """Test generating textmate syntax file with default generator not passing `--name`
    argument.

    Command:
        textX generate --target textmate ./examples/workflow/workflow.tx
    """
    name = lang["name"]
    keywords = lang["keywords"]
    grammar_path = lang["grammar_path"]

    output, err = _textmate_gen_cli(grammar_path)
    assert 'Error: Missing option: "--name".' in output
    assert err.code != 0


def test_textmate_gen_cli_file(lang, tmpdir):
    """Test generating textmate syntax file with default generator and output the
    result to the file.

    Command:
        textX generate --target textmate ./examples/workflow/workflow.tx --name Workflow
        --output-file PATH_TO_TEMP_FILE
    """
    tmp_file = tmpdir.join("syntax.json")

    name = lang["name"]
    keywords = lang["keywords"]
    grammar_path = lang["grammar_path"]

    _textmate_gen_cli(grammar_path, name=name, output_path=str(tmp_file))

    textmate_json = json.load(tmp_file)

    assert textmate_json["name"] == name
    assert textmate_json["scopeName"] == "source." + name

    kw_patterns = _get_keywords_from_textmate(textmate_json)

    assert set(keywords) == set(kw_patterns)


def test_textmate_gen_cli_file_already_exists(lang, tmpdir):
    """Test calling generator two times in a row without --override flag.
    """
    tmp_file = tmpdir.join("syntax.json")

    name = lang["name"]
    keywords = lang["keywords"]
    grammar_path = lang["grammar_path"]

    output, _ = _textmate_gen_cli(grammar_path, name=name, output_path=str(tmp_file))
    output, err = _textmate_gen_cli(grammar_path, name=name, output_path=str(tmp_file))
    assert "Error: File already exists" in output
    assert err.code != 0


def test_textmate_gen_cli_console_with_coloring(lang, coloring_model_path):
    """Test generating textmate syntax file with specific generator, which is not
    currently implemented.

    Command:
        textX generate --target textmate ./examples/workflow/workflow.tx --name Workflow
        --syntax-spec PATH_TO_COLORING_FILE
    """
    name = lang["name"]
    keywords = lang["keywords"]
    grammar_path = lang["grammar_path"]

    _, exc = _textmate_gen_cli(
        grammar_path, name=name, syntax__spec=coloring_model_path
    )
    assert isinstance(exc, NotImplementedError)
