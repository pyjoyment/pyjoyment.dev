# /// script
# dependencies = ["Pyjo-GCP", "Pyjoyment"]
# ///

import Pyjo.GCP.Call
import Pyjo.GCP.Client

from Pyjo.Util import b64_encode
from Pyjoyment.Lite import *

import os


plugin('Health')

# The token of the metadata server of GKE: of the service account of Google that the service account of Kubernetes of
# the pod is bound to, or of the latter itself with Workload Identity Federation for GKE
pubsub = Pyjo.GCP.Client.new(service='pubsub')
topic = os.environ.get('TOPIC', 'events')


# A message of the body of the request, to the topic of the project of the cluster
@post('/events')
async def publish(c):
    credentials = await pubsub.credentials.credentials_p()
    path = f'/v1/projects/{credentials.project}/topics/{topic}:publish'
    message = {'data': b64_encode(c.req.body, ''), 'attributes': {'type': c.req.headers.content_type or ''}}
    result = await pubsub.call_p(Pyjo.GCP.Call.new('POST', path, {'messages': [message]}))
    c.render(json={'id': result['messageIds'][0]}, status=201)


# Who the pod is in Google Cloud, which tells whether the binding works
@get('/whoami')
async def whoami(c):
    credentials = await pubsub.credentials.credentials_p()
    c.render(json={'account': credentials.account, 'project': credentials.project})


app.start()
