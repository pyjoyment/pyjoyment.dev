import Pyjo.File
import Pyjo.JSON.RPC

from Pyjo.MCP.Server import Server
from Pyjoyment.Lite import *

from typing import TypedDict


class Todo(TypedDict):
    file: str
    line: int
    text: str


class Todos(TypedDict):
    todos: list[Todo]


# The directory where the client starts the server, as a local server works with the files of its user
root = Pyjo.File.path().to_abs()
server = Server(name='project', version='1.0.0')


def files(prefix: str = '', arguments: dict[str, str] | None = None) -> list[str]:
    return [name for file in root.list_tree() if (name := '/'.join(file.to_rel(root).to_list())).startswith(prefix)]


@server.tool(annotations={'readOnlyHint': True})
def find_todos(extension: str = 'py') -> Todos:
    """Find the TODO comments in the files of the project.

    :param extension: The extension of the files, without the dot.
    """
    todos = [
        Todo(file=name, line=number, text=line.strip())
        for name in files()
        if root.child(name).extname == extension
        for number, line in enumerate(root.child(name).slurp('UTF-8').splitlines(), 1)
        if 'TODO' in line
    ]
    # The log goes to the standard error, as the standard output has only the messages of MCP
    app.log.info(f'{len(todos)} TODO comments in *.{extension}')
    return Todos(todos=todos)


# A path with .. or an absolute one has no resource, also when it is percent-encoded
@server.resource('file:///project/{+path}', mime_type='text/plain', complete={'path': files})
def project_file(path: str) -> str:
    """A file of the project, by its path."""
    if path not in files():
        uri = f'file:///project/{path}'
        raise Pyjo.JSON.RPC.Error.new(Pyjo.JSON.RPC.INVALID_PARAMS, 'Resource not found', {'uri': uri})
    return root.child(path).slurp('UTF-8')


# The transport stdio, of the command stdio, and Streamable HTTP of the command daemon too
hook('before_server_start', server.to_stdio())
plugin('AllowedHosts')
any('/mcp', server.to_action())

app.start()
