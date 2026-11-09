# A project of Django next to app.py, whose mysite/wsgi.py is the WSGI application
uv add Pyjoyment Django
uv run django-admin startproject mysite .

# Django and Pyjoyment on the server of Pyjoyment, with four workers, instead of gunicorn
uv run app.py prefork -w 4 -l 'http://*:8000'

curl http://127.0.0.1:8000/admin/login/   # Django
curl http://127.0.0.1:8000/readyz         # Pyjoyment
