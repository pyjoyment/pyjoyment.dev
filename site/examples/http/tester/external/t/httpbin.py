import Pyjo.Test.Pyjo

from Pyjo.Test import *

import os


if not os.environ.get('TEST_ONLINE'):
    plan(skip_all='set TEST_ONLINE to enable this test')

# No application, so the URLs are those of the other host, whose certificate is checked, which a test does not by
# default for a server of its own
t = Pyjo.Test.Pyjo.new()
t.ua.insecure = False
t.ua.request_timeout = 20

with subtest('GET with a query'):
    (
        t.get_ok('https://httpbin.org/get', {'Accept': 'application/json'}, form={'q': 'pyjo'})
        .status_is(200)
        .content_type_like(r'^application/json')
        .json_is('/args/q', 'pyjo')
        .json_is('/headers/Accept', 'application/json')
    )

with subtest('POST of JSON'):
    (
        t.post_ok('https://httpbin.org/post', json={'name': 'Sara', 'tags': ['a', 'b']})
        .status_is(200)
        .json_like('/headers/Content-Type', r'^application/json')
        .json_is('/json', {'name': 'Sara', 'tags': ['a', 'b']})
        .json_is('/json/tags/1', 'b')
    )

done_testing()
