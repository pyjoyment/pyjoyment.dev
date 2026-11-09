import Pyjo.App.CGI

from Pyjo.File import curfile
from Pyjoyment.Lite import *


@get('/')
def index(c):
    c.render(text='Hello from Pyjoyment')


# The executable programs of cgi-bin/, in any language, each in a process of its own for each request, without a web
# server of CGI, as Apache was
plugin('Mount', {'/cgi-bin': Pyjo.App.CGI.new(document_root=curfile().sibling('cgi-bin').to_str())})

app.start()
