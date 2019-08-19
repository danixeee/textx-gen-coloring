import json
import re

import pytest
from click.testing import CliRunner
from textx.cli import textx


def _textmate_gen_cli(name, keywords, grammar_path, output_file=None):
    cmd = ["generate", "--target", "textmate", grammar_path, "--name", name]
    if output_file is not None:
        cmd.extend(["--output-path", output_file])

    runner = CliRunner()
    result = runner.invoke(textx, cmd)
    assert result.exit_code == 0

    return result.stdout


def test_textmate_gen_cli_console(lang):
    """
    Test generating textmate syntax file with default generator and output the
    result to the console.

    Command:
        textX generate --target textmate ./examples/workflow/workflow.tx --name Workflow
    """
    name = lang["name"]
    keywords = lang["keywords"]
    grammar_path = lang["grammar_path"]

    output = _textmate_gen_cli(name, keywords, grammar_path)
    for kw in keywords:
        assert kw in output


def test_textmate_gen_cli_file(lang, tmpdir):
    """
    Test generating textmate syntax file with default generator and output the
    result to the file.

    Command:
        textX generate --target textmate ./examples/workflow/workflow.tx --name Workflow
    """
    tmp_file = tmpdir.join("syntax.json")

    name = lang["name"]
    keywords = lang["keywords"]
    grammar_path = lang["grammar_path"]

    _textmate_gen_cli(name, keywords, grammar_path, str(tmp_file))

    textmate_json = json.load(tmp_file)

    assert textmate_json["name"] == name
    assert textmate_json["scopeName"] == "source." + name

    kw_patterns = textmate_json["repository"]["language_keyword"]["patterns"]
    kw_pattern_matches = set(map(lambda x: x["match"], kw_patterns))

    assert keywords == kw_pattern_matches
