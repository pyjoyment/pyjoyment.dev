import Pyjo.App.FastCGI

from Pyjo.File import curfile
from Pyjoyment.Lite import *


# What PHP does not have: a WebSocket on the same server, next to it
@websocket('/ws/echo')
def echo(c):
    c.on('message', lambda c, msg: c.send(f'echo: {msg}'))


# Last, the application of PHP on php-fpm: the files of www/ as they are, and its front controller for every other
# path, as try_files of nginx does; not public/, whose files Pyjoyment serves itself, index.php too
php = Pyjo.App.FastCGI.new(
    url='fcgi://127.0.0.1:9000', document_root=curfile().sibling('www').to_str(), script='index.php', static=True
)
plugin('Mount', {'/': php})

app.start()
