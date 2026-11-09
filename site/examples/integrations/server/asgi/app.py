from Pyjoyment.Lite import *


@get('/')
def index(c):
    c.render(text='Hello from Pyjoyment')


# FastAPI under /api, as a task of asyncio in the event loop of the server, whose /api/docs finds its /api/openapi.json
# with root_path of ASGI
plugin('Mount', {'/api': 'api:api'})

app.start()
