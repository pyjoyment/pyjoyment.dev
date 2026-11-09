uv add Pyjoyment gunicorn
uv run gunicorn

curl http://127.0.0.1:8000/hello/Sara   # {"hello":"Sara","from":"gunicorn\/26.2.0"}
curl http://127.0.0.1:8000/readyz

# The same script, on the server of Pyjoyment, with WebSockets, which WSGI does not have
uv run app.py prefork -l 'http://*:8000'
