python app.py daemon

nc 127.0.0.1 4000                   # a line here comes to the WebSockets too
websocat ws://127.0.0.1:3000/chat   # and a message here to nc
