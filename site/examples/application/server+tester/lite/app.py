from Pyjoyment.Lite import *


app.secrets = ['Change this secret']


@get('/')
def index(c):
    c.render(inline='<h1>Hello <%= name %>!</h1>', name=c.session('user') or 'World')


@post('/login')
def login(c):
    v = c.validation()
    v.required('user').size(1, 20)
    if v.has_error():
        return c.render(json={'error': 'invalid user'}, status=400)
    c.session({'user': v.param('user')})
    c.redirect_to('/')


app.start()
