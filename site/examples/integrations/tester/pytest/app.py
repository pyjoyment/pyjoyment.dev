from Pyjoyment.Lite import *


@get('/hello/:name', {'name': 'World'})
def hello(c):
    c.render(json={'hello': c.param('name')})


@websocket('/echo')
def echo(c):
    c.on('message', lambda c, msg: c.send(f'echo: {msg}'))


app.start()
