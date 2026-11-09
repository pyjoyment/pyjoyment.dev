import Pyjo.Server.Daemon

from Pyjoyment.Lite import *

import asyncio
import contextlib


# A worker of asyncio, whose jobs come from the application of Pyjoyment, and which it reports on
jobs = asyncio.Queue()
done = []


@post('/jobs')
async def enqueue(c):
    await jobs.put(c.req.json())
    c.render(json={'queued': jobs.qsize()}, status=202)


@get('/status')
def status(c):
    c.render(json={'queued': jobs.qsize(), 'done': done})


async def work():
    while True:
        job = await jobs.get()
        await asyncio.sleep(1)
        done.append(job['name'])


# The program of asyncio runs the event loop, where the server of Pyjoyment takes the loop that runs, with its own tasks
async def main():
    with Pyjo.Server.Daemon.new(app=app, listen=['http://127.0.0.1:3000']) as daemon:
        daemon.start()
        await asyncio.gather(work(), work())


# Ctrl-C cancels the tasks, and the end of the block closes the listen sockets
with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
