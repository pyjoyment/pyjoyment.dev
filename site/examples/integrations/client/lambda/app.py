from Pyjoyment.Lite import *

import asyncio


# The words of an answer, each written as it comes, as the tokens of a model are, which a Function URL with the invoke
# mode RESPONSE_STREAM streams to the client
@get('/answer')
async def answer(c):
    c.res.headers.content_type = 'text/plain'
    for word in 'Glue, run and ship Python applications.'.split():
        c.write_chunk(f'{word} '.encode())
        await asyncio.sleep(0.3)
    c.finish()


# The handler "app.handler" of the event function, and the command of the arguments otherwise
handler = app.start()
