# /// script
# requires-python = ">=3.15"
# dependencies = ["Pyjo-AWS"]
# ///

import Pyjo.AWS.Client
import Pyjo.AWS.Protocol.Query
import Pyjo.JSON

from Pyjoyment.Lite import *

import os


# The credentials of the role of the task, of the agent of ECS of AWS_CONTAINER_CREDENTIALS_RELATIVE_URI
sqs = Pyjo.AWS.Client.new(service='sqs')
queue_url = os.environ['QUEUE_URL']

# /livez of the health check of the container of the task definition, as ECS ignores the HEALTHCHECK of the image
plugin('Health')


# A job for the workers of the queue, which the response does not wait for
@post('/jobs')
async def enqueue(c):
    if not isinstance(job := c.req.json(), dict) or 'task' not in job:
        return c.render(json={'error': 'task required'}, status=400)
    params = {'QueueUrl': queue_url, 'MessageBody': Pyjo.JSON.to_json(job)}
    dom = await sqs.call_p(Pyjo.AWS.Protocol.Query.new('SendMessage', params, version='2012-11-05'))
    c.render(json={'id': dom.at('MessageId').text}, status=202)


app.start()
