from Pyjoyment.Lite import *


# What Django does not have: the probes of an orchestrator, and a WebSocket in the same process
plugin('Health')


@websocket('/ws/echo')
def echo(c):
    c.on('message', lambda c, msg: c.send(f'echo: {msg}'))


# Last, Django, which gets every request that the routes before do not match
plugin('Mount', {'/': 'mysite.wsgi:application'})

app.start()
