from Pyjoyment.Lite import *


# What Django does not have without Channels, WebSockets, in a script of Pyjoyment.Lite
@websocket('/echo')
def echo(c):
    c.on('message', lambda c, msg: c.send(f'echo: {msg}'))


@get('/')
def index(c):
    c.render(json={'echo': c.url_for('echo').to_abs()})


app.start()
