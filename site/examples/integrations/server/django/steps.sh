# app.py and t/ in the project of Django, next to its manage.py, whose mysite/wsgi.py is its WSGI application
uv add Pyjoyment
uv run pyjo-prove -l -v t

# Pyjoyment and Django on one server, instead of gunicorn, while the pages move
uv run app.py prefork -w 4 -c 1 -l 'http://*:8000'

# Once every page has moved, the mount goes, and Django with it
