from Pyjoyment.Lite import *


@get('/hello/:name', {'name': 'World'})
def hello(c):
    c.render(json={'hello': c.param('name')})


app.start()
