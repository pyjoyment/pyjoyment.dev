uv add Pyjoyment Flask

# Flask blocks the event loop of its worker while it runs, so each worker of prefork serves one request at a time, as
# a sync worker of gunicorn does
uv run app.py prefork -w 8 -c 1 -l 'http://*:8000'

curl http://127.0.0.1:8000/legacy/              # <a href="/legacy/hello/Sara">Hello</a>
curl http://127.0.0.1:8000/legacy/hello/Sara    # {"from":"Flask","hello":"Sara"}
curl http://127.0.0.1:8000/hello/Sara           # {"hello":"Sara","from":"Pyjoyment"}
