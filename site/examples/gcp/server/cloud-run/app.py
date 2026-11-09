# /// script
# dependencies = ["Pyjo-GCP", "Pyjoyment"]
# ///

import Pyjo.GCP.Call
import Pyjo.GCP.Client

from Pyjo.Util import url_escape
from Pyjoyment.Lite import *

import os


# The startup probe of /readyz and the liveness probe of /livez of Cloud Run
plugin('Health')

# The token of the service account of the service, of the metadata server of Cloud Run, which reads the bucket
storage = Pyjo.GCP.Client.new(service='storage', scopes=['https://www.googleapis.com/auth/devstorage.read_only'])
root = '/storage/v1/b/' + url_escape(os.environ.get('BUCKET', 'mybucket'))


# The objects of the bucket, while the worker serves the other requests
@get('/')
async def index(c):
    call = Pyjo.GCP.Call.new('GET', root + '/o', query={'fields': 'items(name,size,updated)'})
    objects = await storage.call_p(call)
    c.render(json=objects.get('items', []))


app.start()
