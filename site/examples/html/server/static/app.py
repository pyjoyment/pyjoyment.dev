from Pyjoyment.Lite import *


# The files of public/ next to the script, as /css/site.css, which the browsers keep for an hour
@hook('after_static')
def cache(c):
    c.res.headers.cache_control = 'public, max-age=3600'


@get('/')
def index(c):
    c.reply.static('index.html')


app.start()
