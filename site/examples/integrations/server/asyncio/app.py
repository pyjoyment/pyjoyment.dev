import Pyjo.Promise

from Pyjoyment.Lite import *

import asyncio


# A chat of lines on TCP, with the streams of asyncio, and the WebSockets of Pyjoyment, in the same event loop
writers = set()
sockets = set()


def say(line):
    for writer in writers:
        writer.write(f'{line}\n'.encode())
    for c in sockets:
        c.send(line)


async def chat(reader, writer):
    writers.add(writer)
    try:
        while line := await reader.readline():
            say(line.decode().strip())
    finally:
        writers.discard(writer)
        writer.close()


@websocket('/chat')
def websocket_chat(c):
    sockets.add(c)
    c.on('message', lambda c, msg: say(msg))
    c.on('finish', lambda c, *args: sockets.discard(c))


# The server of asyncio, which starts with the one of Pyjoyment, as a task of the loop of the reactor of asyncio
@hook('before_server_start')
def tcp(server, app):
    Pyjo.Promise.new(asyncio.start_server(chat, '127.0.0.1', 4000))


app.start()
