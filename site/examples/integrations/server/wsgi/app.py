from Pyjoyment.Lite import *


plugin('Health')


# The new routes, which Pyjoyment answers already
@get('/hello/:name')
def hello(c):
    c.render(json={'hello': c.param('name'), 'from': 'Pyjoyment'})


# The application of Flask under /legacy, whose url_for links under the prefix, as SCRIPT_NAME of WSGI says it
plugin('Mount', {'/legacy': 'legacy:app'})

app.start()
