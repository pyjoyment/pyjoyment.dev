"""
__DATA__

@@ index.html.ep
<!DOCTYPE html>
<html>
  <head><title>Countdown</title></head>
  <body>
    <p id="count">…</p>
    <script src="<%= url_for('/countdown.js') %>"></script>
  </body>
</html>
"""

import Pyjo.Promise

from Pyjoyment.Lite import *


@get('/')
def index(c):
    c.render('index')


# The events are written as they come, without blocking the other connections
@get('/countdown')
async def countdown(c):
    c.write_sse()
    for n in range(10, 0, -1):
        c.write_sse({'text': str(n)})
        await Pyjo.Promise.timer(1)
    c.write_sse({'type': 'done', 'text': 'Liftoff!'})
    c.finish()


app.start()
