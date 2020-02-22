import sys
from os.path import exists

import click
from textx import LanguageDesc, generator

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
    skip_keywords=False,
    silent=False,
):
    """Generating textmate syntax highlighting from textX grammars"""
    # Check arguments
    if name is None:
        click.echo('\nError: Missing option: "--name".')
        sys.exit(1)

    textmate_json = generate_textmate_syntax(model, name, syntax_spec, skip_keywords)

    if output_path:
        if overwrite is False and exists(output_path):
            click.echo("\nError: File already exists at {}.".format(output_path))
            sys.exit(1)

        with open(output_path, "w") as f:
            f.write(textmate_json)

    else:
        if not silent:
            click.echo(textmate_json)

        return textmate_json
