# /// script
# requires-python = ">=3.15"
# dependencies = ["Pyjo-AWS"]
# ///

import Pyjo.AWS.Client
import Pyjo.AWS.Protocol.JSON

from Pyjoyment.Lite import *

import os


# The credentials of the role of the function and its region, which Lambda gives it in its environment, and Pyjo-AWS
# of the public layer of Pyjoyment
dynamodb = Pyjo.AWS.Client.new(service='dynamodb')
table = os.environ.get('TABLE', 'notes')


def call(operation, **params):
    return Pyjo.AWS.Protocol.JSON.new(f'DynamoDB_20120810.{operation}', {'TableName': table, **params}, version='1.0')


@get('/notes/:id')
async def show(c):
    result = await dynamodb.call_p(call('GetItem', Key={'id': {'S': c.param('id')}}))
    if not (item := result.get('Item')):
        return c.reply.not_found()
    c.render(json={'id': item['id']['S'], 'text': item['text']['S']})


@put('/notes/:id')
async def save(c):
    await dynamodb.call_p(call('PutItem', Item={'id': {'S': c.param('id')}, 'text': {'S': c.req.text}}))
    c.rendered(204)


# The handler "app.handler" of the event function, and the command of the arguments otherwise
handler = app.start()
