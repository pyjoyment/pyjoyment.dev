from Pyjoyment.Lite import *


@get('/hello/:name', {'name': 'World'})
def hello(c):
    c.render(json={'hello': c.param('name')})


# The handler "app.handler" of the event function, and the command of the arguments otherwise
handler = app.start()
