uv add Pyjoyment Pyjo-Reactor-Twisted
uv run app.py

curl http://127.0.0.1:8080/                    # Hello from twisted.web
curl http://127.0.0.1:3000/resolve/localhost   # {"host":"localhost","ip":"127.0.0.1"}
