import Pyjo.Test.Pyjo

from Pyjo.File import curfile
from Pyjo.Test import *


# The application of the script next to the directory of the tests, without a server
t = Pyjo.Test.Pyjo.new(curfile().dirname().sibling('app.py'))

with subtest('Page'):
    t.get_ok('/').status_is(200).text_is('h1', 'Hello World!')

# The test object keeps the cookies, as a browser does
with subtest('Session'):
    t.post_ok('/login', form={'user': ''}).status_is(400).json_is('/error', 'invalid user')
    t.post_ok('/login', form={'user': 'Sara'}).status_is(302).header_is('Location', '/')
    t.get_ok('/').status_is(200).text_is('h1', 'Hello Sara!')

done_testing()
