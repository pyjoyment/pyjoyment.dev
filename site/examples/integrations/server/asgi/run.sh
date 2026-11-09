uv add Pyjoyment FastAPI

# The reactor of asyncio, the default one, as PYJO_REACTOR=Pyjo.Reactor.Poll cannot run an application of ASGI
uv run app.py prefork -w 4 -l 'http://*:8000'

curl http://127.0.0.1:8000/api/items/1   # {"id":1,"name":"Pen"}
open http://127.0.0.1:8000/api/docs      # Swagger UI of FastAPI
