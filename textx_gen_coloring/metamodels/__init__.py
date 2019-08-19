from os.path import dirname, join

from textx import metamodel_from_file

mm_path = dirname(__file__)


def _get_metamodel(file_name):
    return metamodel_from_file(join(mm_path, file_name))


coloring_mm = _get_metamodel("coloring.tx")
textx_mm = _get_metamodel("textx.tx")
