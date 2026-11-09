from Pyjoyment.Lite import *

import platform


plugin('Health')


@get('/')
def index(c):
    c.render(json={'hello': platform.system(), 'python': platform.python_version()})


app.start()
