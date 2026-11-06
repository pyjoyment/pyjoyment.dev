from Pyjoyment.Lite import *

import platform


# The files of public/ change only with a deployment, so CloudFront and the browsers keep them for an hour, where a
# response of an action has no Cache-Control and is not cached
@hook('after_static')
def cache_static(c):
    c.res.headers.cache_control = 'public, max-age=3600'


@get('/')
def index(c):
    c.render('index')


# /hello and /hello/Sara, rendered by the function on each request
@get('/hello/:name', {'name': 'World'}, 'hello')
def hello(c):
    c.render(json={'hello': c.param('name'), 'python': platform.python_version()})


# The handler "app.handler" of the event function, and the command of the arguments otherwise
handler = app.start()
