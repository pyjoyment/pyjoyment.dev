# /// script
# requires-python = ">=3.15"
# dependencies = ["Pyjo-AWS"]
# ///

import Pyjo.AWS.Client
import Pyjo.AWS.Protocol.JSON

from Pyjoyment.Lite import *


# The credentials of the role of the instance profile, of the instance metadata of EC2 with a token of IMDSv2, and the
# region of AWS_REGION of the unit of systemd
ssm = Pyjo.AWS.Client.new(service='ssm')

# The secrets of the signed cookies, of a SecureString of Parameter Store, the newest one first, read once by the
# manager of prefork, before its workers
call = Pyjo.AWS.Protocol.JSON.new('AmazonSSM.GetParameter', {'Name': '/myapp/secrets', 'WithDecryption': True})
app.secrets = ssm.call(call)['Parameter']['Value'].split(',')


@get('/')
def index(c):
    visits = c.session('visits') or 0
    c.session(visits=visits + 1).render(json={'visits': visits + 1})


app.start()
