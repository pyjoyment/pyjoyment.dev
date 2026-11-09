uv add Pyjoyment 'uvicorn[standard]'

# The event loop of uvicorn, uvloop with uvicorn[standard], which the reactor of asyncio takes
PYJO_ASGI=1 uv run uvicorn app:application --workers 4 --port 8000

curl -N http://127.0.0.1:8000/count   # an event every half a second
websocat ws://127.0.0.1:8000/echo
