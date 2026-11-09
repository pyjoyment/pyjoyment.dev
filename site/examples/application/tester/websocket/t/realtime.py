import Pyjo.Test.Pyjo

from Pyjo.Test import *
from Pyjoyment.Lite import *


@websocket('/echo')
def echo(c):
    c.on('message', lambda c, msg: c.send(f'echo: {msg}'))


# The event json decodes each message, as message gives it as it is
@websocket('/echo.json')
def echo_json(c):
    c.on('json', lambda c, doc: c.send({'json': {'echo': doc}}))


@get('/events')
def events(c):
    c.write_sse()
    for n in range(1, 4):
        c.write_sse({'text': str(n)})
    c.finish()


t = Pyjo.Test.Pyjo.new()

with subtest('WebSocket'):
    t.websocket_ok('/echo').send_ok('hi').message_ok().message_is('echo: hi').finish_ok()
    t.websocket_ok('/echo.json').send_ok({'json': {'n': 1}}).message_ok().json_message_is('/echo/n', 1).finish_ok()

with subtest('Server-Sent Events'):
    t.get_sse_ok('/events').status_is(200)
    t.sse_ok().sse_text_is('1').sse_ok().sse_text_is('2').sse_ok().sse_text_is('3').sse_finished_ok()

done_testing()
