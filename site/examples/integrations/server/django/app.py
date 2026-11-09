from Pyjoyment.Lite import *


# The pages that have moved from Django already, one route at a time, ahead of it
@get('/about')
def about(c):
    c.render(inline='<h1>About us</h1><p>Rendered by <%= engine %></p>', engine='Pyjoyment')


@get('/api/status')
def status(c):
    c.render(json={'status': 'ok'})


# Django, as it was, with every page that has not moved yet; its views, templates and admin stay as they are
plugin('Mount', {'/': 'mysite.wsgi:application'})

app.start()
