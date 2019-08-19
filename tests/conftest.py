from pathlib import Path

import pytest

DATA_PATH = Path(__file__).parent.resolve() / "data"

TEST_DATA = {
    "Robot": {
        "name": "Robot",
        "keywords": set(["begin", "end", "initial", "up", "down", "left", "right", ","]),
        "grammar_path": str(DATA_PATH / "robot.tx"),
    }
}


def pytest_generate_tests(metafunc):
    if "lang" in metafunc.fixturenames:
        metafunc.parametrize("lang", TEST_DATA.keys(), indirect=True)


@pytest.fixture
def lang(request):
    return TEST_DATA.get(request.param)
