uv add Django Pyjoyment 'uvicorn[standard]'
uv run uvicorn mysite.asgi:application --workers 4

curl http://127.0.0.1:8000/admin/login/   # Django
curl http://127.0.0.1:8000/realtime/      # {"echo":"ws:\/\/127.0.0.1:8000\/realtime\/echo"}
websocat ws://127.0.0.1:8000/realtime/echo
