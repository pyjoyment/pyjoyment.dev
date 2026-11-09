import Pyjo.Test.Pyjo

from Pyjo.File import curfile
from Pyjo.Test import *


# Both of them, without a server, so that a page that moves keeps its test
t = Pyjo.Test.Pyjo.new(curfile().dirname().sibling('app.py'))

with subtest('Pyjoyment'):
    t.get_ok('/about').status_is(200).text_is('h1', 'About us')
    t.get_ok('/api/status').status_is(200).json_is('/status', 'ok')

with subtest('Django'):
    t.get_ok('/admin/login/').status_is(200).text_like('title', r'Django site admin')
    t.get_ok('/admin/').status_is(302).header_like('Location', r'^/admin/login/')

done_testing()
