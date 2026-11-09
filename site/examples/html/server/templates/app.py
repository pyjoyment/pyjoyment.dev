from Pyjoyment.Lite import *


app.secrets = ['Change this secret']

items = ['Bread', 'Milk']


# templates/index.html.ep, with the values of the stash as its variables
@get('/')
def index(c):
    c.render('index', items=items)


# The form of the template posts here, as form_for takes the method of the route named "add"
@post('/', 'add')
def add(c):
    v = c.validation()
    if v.csrf_protect().has_error('csrf_token'):
        return c.render(text='Bad CSRF token', status=403)
    v.required('item', 'trim', 'not_empty').size(1, 30)
    if v.has_error():
        return c.render('index', items=items, status=400)
    items.append(v.param('item'))
    c.flash(added=v.param('item'))
    c.redirect_to('/')


app.start()
