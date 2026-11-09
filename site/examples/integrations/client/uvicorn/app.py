from Pyjoyment.Lite import *

import asyncio


# The startup of the lifespan of uvicorn, as of the servers of Pyjoyment, and after_server_stop of its shutdown
@hook('before_server_start')
def start(server, app):
    app.log.info(f'Started on {type(server).__module__}')


@websocket('/echo')
def echo(c):
    c.on('message', lambda c, msg: c.send(f'echo: {msg}'))


@get('/count')
async def count(c):
    c.write_sse()
    for n in range(1, 4):
        c.write_sse({'text': str(n)})
        await asyncio.sleep(0.5)
    c.finish()


# The ASGI application with PYJO_ASGI, for uvicorn, and the command of the arguments otherwise
application = app.start()
