import Pyjo.GCP.Call
import Pyjo.GCP.Client

from Pyjo.Util import b64_decode
from Pyjoyment.Lite import *


# A secret of Secret Manager, with the token of the service account of the instance, of its metadata server, once, in
# the manager of prefork before it forks its workers
def secret(name):
    client = Pyjo.GCP.Client.new(service='secretmanager')
    project = client.credentials.credentials().project
    path = f'/v1/projects/{project}/secrets/{name}/versions/latest:access'
    return b64_decode(client.call(Pyjo.GCP.Call.new('GET', path))['payload']['data']).decode()


# The secret of the signed cookies, the same on every instance behind the load balancer
app.secrets = [secret('myapp-session')]


@get('/')
def index(c):
    visits = c.session('visits') or 0
    c.session(visits=visits + 1)
    c.render(text=f'Visit {visits + 1} of this browser, on any instance')


app.start()
