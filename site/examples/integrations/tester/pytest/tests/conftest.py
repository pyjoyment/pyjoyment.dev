from Pyjo.File import curfile

import pytest


# The application of the fixture t, which the plugin of pytest of Pyjoyment gives the tests
@pytest.fixture
def app():
    return curfile().dirname().sibling('app.py')
