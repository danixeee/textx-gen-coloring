from functools import partial
from os.path import dirname, exists, join

import click
from textx import LanguageDesc, generator, metamodel_from_file

from .generators import generate_textmate_syntax
from .metamodels import coloring_mm

coloring_lang = LanguageDesc(
    name="txcl",
    pattern="*.txcl",
    description="A language for syntax highlight definition.",
    metamodel=coloring_mm,
)


@generator("textX", "textmate")
def textmate_gen(
    metamodel,
    model,
    output_path="",
    overwrite=False,
    debug=False,
    name=None,
    syntax_spec=None,
):
    """Generating textmate syntax highlighting from textX grammars"""
    # Check arguments
    if name is None:
        click.echo('\nError: Missing argument: "name".')
        return

    textmate_json = generate_textmate_syntax(model, name, syntax_spec)

    if output_path:
        if overwrite is False and exists(output_path):
            raise Exception("File already exists.")

        with open(output_path, "w") as f:
            f.write(textmate_json)

    else:
        click.echo(textmate_json)
