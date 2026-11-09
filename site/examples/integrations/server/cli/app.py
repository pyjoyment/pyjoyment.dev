import Pyjo.IOLoop

from Pyjoyment.Lite import *


# The output of a program, streamed as it comes, without blocking the other connections
@get('/ping/#host', host=['127.0.0.1', 'example.com'])
def ping(c):
    c.render_later()
    c.res.headers.content_type = 'text/plain'
    child = Pyjo.IOLoop.spawn(['ping', '-c', '3', c.param('host')])
    child.on('spawn', lambda child: child.stdout.on('read', lambda stream, chunk: c.write_chunk(chunk)))
    child.on('close', lambda child, code, signal: c.write_chunk(b''))
    child.on('error', lambda child, err: c.reply.exception(err))


# An interactive program, as the calculator bc, on a WebSocket: a message to its standard input, a line of its output
# to the browser, as long as the WebSocket is open
@websocket('/bc')
def bc(c):
    child = Pyjo.IOLoop.spawn(['bc', '-l'])
    child.on('spawn', lambda child: child.stdout.on('read', lambda stream, chunk: c.send(chunk.decode().strip())))
    c.on('message', lambda c, msg: child.stdin.write(f'{msg}\n'.encode()))
    c.on('finish', lambda c, *args: child.kill())


app.start()
