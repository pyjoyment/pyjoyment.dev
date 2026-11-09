import Pyjo.IOLoop
import Pyjo.IOLoop.Messages
import Pyjo.MCP
import Pyjo.Promise

from Pyjo.JSON.RPC import RPC

import sys


# Pyjo.MCP.Client speaks Streamable HTTP, so over stdio the requests are those of JSON-RPC, each with the _meta of MCP
META = {
    Pyjo.MCP.META_PROTOCOL_VERSION: Pyjo.MCP.PROTOCOL_VERSION,
    Pyjo.MCP.META_CLIENT_CAPABILITIES: {},
    Pyjo.MCP.META_CLIENT_INFO: {'name': 'stdio-client', 'version': '1.0.0'},
}

# The server in a child process, a message on each line of its standard input and output, and its log on its error
child = Pyjo.IOLoop.spawn([sys.executable, 'app.py', 'stdio'])
child.stderr.on('read', lambda stream, chunk: sys.stderr.buffer.write(chunk))
messages = Pyjo.IOLoop.Messages.new(child.stdout, output=child.stdin)
server = RPC().serve(messages)


@Pyjo.Promise.coroutine
async def main():
    for tool in (await server.call_p('tools/list', _meta=META))['tools']:
        print(f'{tool["name"]}: {tool["description"]}')

    result = await server.call_p('tools/call', name='find_todos', arguments={'extension': 'py'}, _meta=META)
    for todo in result['structuredContent']['todos']:
        print(f'{todo["file"]}:{todo["line"]}: {todo["text"]}')

    # The end of its standard input ends the server, once it has answered
    closed = child.once_p('close')
    messages.close_gracefully()
    await closed


main().wait()
