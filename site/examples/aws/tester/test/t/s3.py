"""
__DATA__

@@ list.xml.ep
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
% for key in keys:
  <Contents><Key><%= key %></Key></Contents>
% end
</ListBucketResult>

@@ error.xml.ep
<Error><Code><%= code %></Code><Message><%= message %></Message></Error>
"""

import Pyjo.AWS.Client
import Pyjo.AWS.Credentials
import Pyjo.AWS.Credentials.Static
import Pyjo.AWS.Error
import Pyjo.Test.Pyjo

from Pyjo.Test import *
from Pyjoyment.Lite import *

import re

from notes import Notes


# S3 of the test, of a bucket in memory, which takes the requests signed with the key of the test only
bucket = {}


@under
def signed(c):
    if (c.req.headers.authorization or '').startswith('AWS4-HMAC-SHA256 Credential=AKIDTEST/'):
        return True
    c.render('error', format='xml', status=403, code='AccessDenied', message='Access Denied')


@get('/mybucket')
def list_objects(c):
    c.render('list', format='xml', keys=sorted(key for key in bucket if key.startswith(c.param('prefix'))))


@any(['GET', 'PUT'], '/mybucket/*key')
def object_(c):
    key = c.param('key')
    if c.req.method == 'PUT':
        bucket[key] = c.req.body
        return c.rendered(200)
    if key not in bucket:
        return c.render('error', format='xml', status=404, code='NoSuchKey', message='No such key')
    c.render(data=bucket[key], format='txt')


t = Pyjo.Test.Pyjo.new()


# A client of the user agent of the test, whose relative endpoint is its server of the application of the test
def s3(key):
    credentials = Pyjo.AWS.Credentials.new(access_key_id=key, secret_access_key='secret')
    provider = Pyjo.AWS.Credentials.Static.new(credentials)
    return Pyjo.AWS.Client.new(service='s3', region='eu-central-1', endpoint='/', credentials=provider, ua=t.ua)


notes = Notes('mybucket', s3('AKIDTEST'))

with subtest('Save and load'):
    notes.save('hello.txt', 'Hello, S3!')
    is_ok(bucket['notes/hello.txt'], b'Hello, S3!', 'object in the bucket')
    is_ok(notes.load('hello.txt'), 'Hello, S3!', 'note loaded')
    is_deeply_ok(notes.names(), ['hello.txt'], 'notes listed')

with subtest('Missing'):
    is_ok(notes.load('missing.txt'), None, 'no note of NoSuchKey')

with subtest('Access denied'):
    throws_ok(lambda: Notes('mybucket', s3('AKIDOTHER')).load('hello.txt'), Pyjo.AWS.Error.object, 'error of AWS')
    throws_ok(lambda: Notes('mybucket', s3('AKIDOTHER')).load('hello.txt'), re.compile(r'^AccessDenied:'), 'its code')

done_testing()
