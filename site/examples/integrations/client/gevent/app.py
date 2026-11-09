import os


# The reactor of Pyjoyment on gevent, selected before Pyjo.IOLoop is loaded
os.environ['PYJO_REACTOR'] = 'Pyjo.Reactor.Gevent'

import Pyjo.Promise  # noqa: E402
import Pyjo.UserAgent  # noqa: E402

from Pyjoyment.Lite import *  # noqa: E402

import gevent  # noqa: E402


# A service that takes its time, of the application itself
@get('/slow/<n:num>')
async def slow(c):
    await Pyjo.Promise.timer(int(c.param('n')) / 10)
    c.render(json={'n': int(c.param('n'))})


# Code that blocks, as it is written, in greenlets, which wait in the hub of gevent, where the server runs, without
# blocking the other connections
def fetch(base, n):
    with Pyjo.UserAgent.new() as ua:
        return ua.get(f'{base}/slow/{n}').result.json('/n')


@get('/')
def index(c):
    base = c.req.url.to_abs().base
    greenlets = [gevent.spawn(fetch, base, n) for n in (3, 1, 2)]
    gevent.spawn(lambda: (gevent.joinall(greenlets), c.render(json=[g.value for g in greenlets])))


app.start()
