import asyncio

from contextlib import asynccontextmanager

from fastapi import FastAPI


# The lifespan starts with the first request of each worker, and ends with the graceful stop of the server
@asynccontextmanager
async def lifespan(app):
    app.state.items = {1: 'Pen'}
    yield
    app.state.items.clear()


api = FastAPI(lifespan=lifespan)


@api.get('/items/{id}')
async def item(id: int):
    await asyncio.sleep(0.1)
    return {'id': id, 'name': api.state.items.get(id)}
