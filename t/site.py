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
        t.get_ok('/').status_is(200).content_type_like(r'^text/html').header_is('Cache-Control', 'public, max-age=3600')
        t.element_exists('h1 img[alt="Pyjoyment"]')
        t.text_is('.tagline', 'Glue, run and ship Python applications. Zero dependencies.')
        t.text_is('.feature[href="/http"]', 'HTTP').text_is('.role[href="/server"]', 'Server')
        t.element_exists_not('[aria-current]').element_exists_not('.scenarios')

    with subtest('Feature'):
        t.get_ok('/http').status_is(200).text_is('title', 'HTTP | Pyjoyment')
        t.text_is('.feature[aria-current]', 'HTTP').attr_is('.feature[aria-current]', 'href', '/')
        t.attr_is('[data-id="role-server"]', 'href', '/http/server')

    with subtest('Role'):
        t.get_ok('/server').status_is(200).text_is('.role[aria-current]', 'Server')
        t.attr_is('.role[aria-current]', 'href', '/').attr_is('[data-id="role-tester"]', 'href', '/tester')

        # Another role replaces the one selected
        t.get_ok('/application/tester').status_is(200).text_is('title', 'Application Tester | Pyjoyment')
        t.attr_is('link[rel="canonical"]', 'href', 'https://pyjoyment.dev/application/tester')
        t.attr_is('[data-id="role-server"]', 'href', '/application/server')
        t.attr_is('[data-id="role-tester"]', 'href', '/application')
        t.attr_is('[data-id="feature-http"]', 'href', '/http/tester')
        t.text_is('.scenario[href="/application/tester/test"]', 'Test of an application')

        t.get_ok('/application/server+tester').status_is(404)

    with subtest('Scenario'):
        t.get_ok('/http/server/lambda').status_is(200).text_is('.scenario[aria-current]', 'AWS Lambda function')
        t.text_is('title', 'HTTP Server: AWS Lambda function | Pyjoyment')
        t.text_is('#tab-0', 'app.py').text_is('#tab-1', 'build.sh')
        t.text_like('#panel-0 code.language-python', r'handler = app\.start\(\)')
        t.element_exists('#panel-1 code.language-bash')

        # The actions of a file: the clipboard, and its source on GitHub
        t.text_is('#panel-0 .copy', 'Copy')
        source = 'https://github.com/pyjoyment/pyjoyment.dev/blob/main/site/examples/http/server/lambda/app.py'
        t.attr_is('#panel-0 a.source', 'href', source).attr_is('#panel-0 a.source', 'target', '_blank')

        # The order and the titles of the tabs of the catalog
        t.get_ok('/mcp/cli/claude').status_is(200).text_is('#tab-0', 'claude.sh').text_is('#tab-1', '.mcp.json')

        t.get_ok('/http/server/missing').status_is(404).header_is('Cache-Control', None)
        t.get_ok('/missing/server').status_is(404)

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
