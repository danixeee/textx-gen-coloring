from .templates import jinja_env, textmate_template_dir


class TextmateGen:
    _template = jinja_env.get_template('textmate/language.json.template')

    @staticmethod
    def generate(strings):
        def get_kw_name(s):
            import re
            return {
                0: 'constant.language',
                1: 'support.class'
            }.get(bool(re.match("^[a-zA-Z0-9_]*$", s)))

        keywords = [{'name': get_kw_name(s), 'match': s} for s in strings]

        coloring_model = {
            'name': 'Workflow',
            'extensions': ["wf"],
            'comment': {
                'line': "//",
                'block_start': "/*",
                'block_end': "*/"
            },
            'keywords': keywords,
            'operations': [],
            'regular_expressions': []
        }
        print(TextmateGen._template.render(coloring_model))
