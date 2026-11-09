import os


# The reactor of Pyjoyment on the reactor of Twisted, selected before Pyjo.IOLoop is loaded
os.environ['PYJO_REACTOR'] = 'Pyjo.Reactor.Twisted'

import Pyjo.Reactor.Twisted  # noqa: E402


# The reactor of Twisted of poll or select, before Twisted is imported, which would install its default, epoll on Linux
Pyjo.Reactor.Twisted.install()

import Pyjo.Server.Daemon  # noqa: E402

from Pyjoyment.Lite import *  # noqa: E402

from twisted.internet import reactor  # noqa: E402
from twisted.web import resource, server  # noqa: E402


# The application of Twisted, as it was
class Legacy(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        return b'Hello from twisted.web'


# An action that renders once a Deferred of Twisted fires, as the event loop is the same
@get('/resolve/#host')
def resolve(c):
    c.render_later()
    deferred = reactor.resolve(c.param('host'))
    deferred.addCallbacks(
        lambda ip: c.render(json={'host': c.param('host'), 'ip': ip}),
        lambda failure: c.render(json={'error': failure.getErrorMessage()}, status=502),
    )


reactor.listenTCP(8080, server.Site(Legacy()))

# Twisted runs the event loop, with the server of Pyjoyment in it, until Ctrl-C, and the end of the block closes its
# listen sockets
with Pyjo.Server.Daemon.new(app=app, listen=['http://*:3000']) as daemon:
    daemon.start()
    reactor.run()
