from . import generator


@generator('textX', 'textmate')
def textmate(cl_model, metamodel, model, output_path, overwrite, debug=False):
    """Generating textmate syntax highlighting from textX grammars"""
    print(cl_model)
