"""
__DATA__

@@ index.html.ep
% layout('default')
% title('Hello')
<p>Hello <%= name %>!</p>
<p><%= link_to('As JSON', 'hello', name=name) %></p>

@@ layouts/default.html.ep
<!DOCTYPE html>
<html>
  <head><title><%= c.title() %></title></head>
  <body><%= content() %></body>
</html>
"""

from Pyjoyment.Lite import *


@get('/')
def index(c):
    c.render('index', name=c.param('name') or 'World')


@get('/hello/:name', 'hello')
def hello(c):
    c.render(json={'hello': c.param('name')})


app.start()
