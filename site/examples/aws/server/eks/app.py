# /// script
# requires-python = ">=3.15"
# dependencies = ["Pyjo-AWS"]
# ///

import Pyjo.AWS.Client
import Pyjo.AWS.Protocol.RestXML

from Pyjo.Util import url_escape
from Pyjoyment.Lite import *

import os


# The credentials of the role of the service account of the pod, which EKS gives it in its environment: of IRSA,
# AWS_ROLE_ARN and AWS_WEB_IDENTITY_TOKEN_FILE, or of EKS Pod Identity, AWS_CONTAINER_CREDENTIALS_FULL_URI
s3 = Pyjo.AWS.Client.new(service='s3')
root = '/' + url_escape(os.environ['BUCKET'])

# The probes of Kubernetes, whose readiness waits for the bucket, and so for the role of the pod
plugin('Health', checks={'s3': lambda c: s3.call_p(Pyjo.AWS.Protocol.RestXML.new('HEAD', root))})


@get('/files')
async def files(c):
    call = Pyjo.AWS.Protocol.RestXML.new('GET', root, query={'list-type': 2, 'prefix': c.param('prefix') or ''})
    dom = await s3.call_p(call)
    c.render(json={'files': dom.find('Contents > Key').map('text').to_list()})


app.start()
