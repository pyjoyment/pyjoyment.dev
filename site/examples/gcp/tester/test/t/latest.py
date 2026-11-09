import Pyjo.GCP.Client
import Pyjo.GCP.Credentials
import Pyjo.GCP.Credentials.Provider
import Pyjo.GCP.Error
import Pyjo.UserAgent

from Pyjo.Test import *
from Pyjoyment.Lite import *

import reports


REPORTS = [
    {'name': 'daily/2026-11-08.csv', 'updated': '2026-11-08T06:00:00.000Z'},
    {'name': 'daily/2026-11-09.csv', 'updated': '2026-11-09T06:00:00.000Z'},
]


def error(c, code, message, reason):
    c.render(json={'error': {'code': code, 'message': message, 'errors': [{'reason': reason}]}}, status=code)


# Cloud Storage of the test, which takes the token of the test only
@get('/storage/v1/b/<bucket>/o')
def list_objects(c):
    if c.req.headers.authorization != 'Bearer ya29.test':
        return error(c, 401, 'Invalid Credentials', 'authError')
    if c.param('bucket') != 'reports':
        return error(c, 404, 'The specified bucket does not exist.', 'notFound')
    prefix = c.param('prefix') or ''
    c.render(json={'items': [item for item in REPORTS if item['name'].startswith(prefix)]})


# A token of the test, in the place of the Application Default Credentials
class Token(Pyjo.GCP.Credentials.Provider.object):
    async def fetch(self):
        return Pyjo.GCP.Credentials.new(token='ya29.test')


# The empty endpoint is the server of the user agent, which serves the application of the test without a port
ua = Pyjo.UserAgent.new()
ua.server.app = app
storage = Pyjo.GCP.Client.new(service='storage', endpoint='', credentials=Token(), ua=ua)

is_ok(reports.latest(storage, 'reports', 'daily/'), 'daily/2026-11-09.csv', 'newest report')
none_ok(reports.latest(storage, 'reports', 'weekly/'), 'no report')

e = throws_ok(lambda: reports.latest(storage, 'missing', ''), Pyjo.GCP.Error.object, 'error of the API').got
is_ok(e.code, 404, 'status of HTTP')
is_ok(e.reason, 'notFound', 'reason of Cloud Storage')

done_testing()
