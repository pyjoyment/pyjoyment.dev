from Pyjo.JSON.Schema import Schema
from Pyjoyment.Lite import *

from typing import NotRequired, TypedDict


class Item(TypedDict):
    name: str
    price: float
    tags: NotRequired[list[str]]


# JSON Schema 2020-12 of the type hints
ITEM = Schema.of(Item)

items = {1: {'name': 'Pen', 'price': 1.5}}


@get('/items')
def index(c):
    c.render(json=[{'id': id, **item} for id, item in items.items()])


@post('/items')
def create(c):
    item = c.req.json()
    if not (result := ITEM.validate(item)):
        # As "/price: Expected number - got string."
        return c.render(json={'errors': [str(error) for error in result.errors]}, status=422)
    id = max(items, default=0) + 1
    items[id] = item
    c.res.headers.location = c.url_for('item', id=id).to_abs()
    c.render(json={'id': id, **item}, status=201)


@get('/items/<id:num>', 'item')
def show(c):
    if (item := items.get(int(c.param('id')))) is None:
        return c.reply.json_not_found()
    c.render(json={'id': int(c.param('id')), **item})


app.start()
