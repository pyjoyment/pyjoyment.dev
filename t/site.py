import Pyjo.App.Lambda
import Pyjo.Test.Pyjo

from Pyjo.File import curfile
from Pyjo.Test import *

import os


# The application of site/, as a server of its own, and as the event function of the Function URL behind CloudFront,
# with its events, as Lambda runs it
SITE = curfile().dirname().sibling('site')


def check(t: Pyjo.Test.Pyjo.object) -> None:
    with subtest('Page'):
        t.get_ok('/').status_is(200).content_type_like(r'^text/html')
        t.text_is('h1 a[href="https://github.com/pyjoyment/Pyjoyment"]', 'I ❤️ Pyjoyment')

    with subtest('Dynamic'):
        t.get_ok('/hello').status_is(200).json_is('/hello', 'World').header_is('Cache-Control', None)
        t.get_ok('/hello/Sara').status_is(200).json_is('/hello', 'Sara')

    with subtest('Static'):
        t.get_ok('/css/site.css').status_is(200).content_type_like(r'^text/css')
        t.header_is('Cache-Control', 'public, max-age=3600')

    with subtest('Not found'):
        t.get_ok('/missing').status_is(404)


with subtest('Server'):
    check(Pyjo.Test.Pyjo.new(SITE.child('app.py')))

if os.name == 'nt':
    skip('Lambda functions need pipes that the event loop watches, which Windows does not have')
else:
    with subtest('Function'):
        env = {'PYJO_MODE': 'production'}
        with Pyjo.App.Lambda.new(function='app.handler', task_root=SITE.to_str(), payload='2.0', env=env) as function:
            check(Pyjo.Test.Pyjo.new(function))

done_testing()
