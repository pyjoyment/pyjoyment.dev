"""
__DATA__

@@ index.html.ep
<!DOCTYPE html>
<html>
  <head><title>Echo</title></head>
  <body>
    <input id="message" placeholder="Say something">
    <ul id="log"></ul>
    <script src="<%= url_for('/echo.js') %>"></script>
  </body>
</html>
"""

from Pyjoyment.Lite import *


@get('/')
def index(c):
    c.render('index')


# Each message comes back, as text or as JSON
@websocket('/echo')
def echo(c):
    @c.on('message')
    def message(c, msg):
        c.send(f'echo: {msg}')


app.start()
