from Pyjoyment.Lite import *


plugin('Health')


@get('/hello/:name', {'name': 'World'})
def hello(c):
    c.render(json={'hello': c.param('name'), 'from': c.req.env.get('SERVER_SOFTWARE')})


# The WSGI application with PYJO_WSGI, for gunicorn, and the command of the arguments otherwise
application = app.start()
