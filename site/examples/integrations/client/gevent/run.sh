uv add Pyjoyment Pyjo-Reactor-Gevent

uv run app.py prefork -w 4

curl http://127.0.0.1:3000/   # [3,1,2] after 0.3 seconds, not 0.6
