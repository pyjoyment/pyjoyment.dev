from Pyjoyment.Lite import *


@get('/hello/:name', {'name': 'World'})
def hello(c):
    c.render(json={'hello': c.param('name')})


@post('/items')
def create(c):
    if not (name := c.req.json('/name')):
        return c.render(json={'error': 'name required'}, status=400)
    c.render(json={'name': name}, status=201)


app.start()
