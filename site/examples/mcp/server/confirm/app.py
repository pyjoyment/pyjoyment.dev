from Pyjo.MCP.Server import Server
from Pyjo.MCP.Tool import Error
from Pyjoyment.Lite import *


server = Server(name='files', version='1.0.0')
files = {'notes.txt': 'Buy milk', 'todo.txt': 'Call the plumber'}


@server.tool(context=True, annotations={'destructiveHint': True})
def delete_file(context, name: str) -> str:
    """Delete a file, once the user confirms it.

    :param name: The name of the file.
    """
    if name not in files:
        raise Error.new(f'No such file: {name}')
    # The result input_required asks the client, which sends the same request again with the answer, so the function
    # runs from its beginning again, and deletes only after the question
    if context.elicit('confirm', f'Delete {name}?')['action'] != 'accept':
        return f'Kept {name}'
    del files[name]
    return f'Deleted {name}'


# The secrets sign the requestState, the answers of the rounds before, which the client sends back
app.secrets = ['s3cret']
plugin('AllowedHosts')

any('/mcp', server.to_action())

app.start()
