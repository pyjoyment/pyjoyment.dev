# Pyjoyment, and the reactor of Winloop, the fork of uvloop for Windows
uv add Pyjoyment Pyjo-Reactor-Winloop

# Threads instead of the processes of prefork, which needs fork, that Windows does not have
$env:PYJO_REACTOR = 'Pyjo.Reactor.Winloop'
uv run app.py prethread -w 8 -l 'http://*:8080'

# Ctrl-C or Ctrl-Break stops it gracefully
Invoke-RestMethod http://127.0.0.1:8080/
