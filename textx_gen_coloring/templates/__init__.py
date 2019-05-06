from os.path import dirname, join

import jinja2

templates_path = dirname(__file__)

textmate_template_dir = join(templates_path, 'textmate')

jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(templates_path),
    autoescape=True,
    lstrip_blocks=True,
    trim_blocks=True)
