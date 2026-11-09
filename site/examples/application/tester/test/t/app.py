import Pyjo.Test.Pyjo

from Pyjo.Test import *
from Pyjoyment.Lite import *


# The application of the test itself, without a server
@get('/hello/:name', {'name': 'World'})
def hello(c):
    c.render(json={'hello': c.param('name')})


@post('/items')
def create(c):
    if not (name := c.req.json('/name')):
        return c.render(json={'error': 'name required'}, status=400)
    c.render(json={'name': name}, status=201)


t = Pyjo.Test.Pyjo.new()

with subtest('Hello'):
    t.get_ok('/hello').status_is(200).json_is('/hello', 'World')
    t.get_ok('/hello/Sara').status_is(200).json_is({'hello': 'Sara'})

with subtest('Items'):
    t.post_ok('/items', json={'name': 'Pen'}).status_is(201).json_is('/name', 'Pen')
    t.post_ok('/items', json={}).status_is(400).json_is('/error', 'name required')

with subtest('Not found'):
    t.get_ok('/missing').status_is(404)

done_testing()
