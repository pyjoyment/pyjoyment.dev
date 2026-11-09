from Pyjoyment.Lite import *

import os


# The files of DOCUMENT_ROOT before the ones of public/ next to the script, with ranges and ETags
app.static.paths.insert(0, os.environ.get('DOCUMENT_ROOT', '/var/www'))


@hook('after_static')
def cache(c):
    c.res.headers.cache_control = 'public, max-age=3600'


# The hook after_static is the one of the files of the paths, not of reply.static of an action
@get('/')
def index(c):
    c.res.headers.cache_control = 'public, max-age=3600'
    c.reply.static('index.html')


app.start()
