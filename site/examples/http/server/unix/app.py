from Pyjoyment.Lite import *


# The settings of pyjo-hot, on a socket of UNIX behind nginx
app.config(hot={'listen': ['http+unix://%2Frun%2Fmyapp%2Fhttp.sock'], 'workers': 8, 'proxy': True})


@get('/')
def index(c):
    c.render(text=f'Hello {c.tx.remote_address}')


app.start()
