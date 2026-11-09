import Pyjo.MCP.Test

from Pyjo.MCP.Server import Server
from Pyjo.MCP.Tool import Error
from Pyjo.Test import *
from Pyjoyment.Lite import *

from typing import Literal


server = Server(name='notes', version='1.0.0')
notes = ['Buy milk']


@server.tool
def add_note(text: str) -> int:
    """Add a note, and return its number."""
    notes.append(text)
    return len(notes)


@server.tool
def delete_note(number: int) -> str:
    """Delete a note, by its number."""
    if not 0 < number <= len(notes):
        raise Error.new(f'No note {number}')
    return f'Deleted "{notes.pop(number - 1)}"'


@server.prompt
def summarize(style: Literal['short', 'detailed'] = 'short') -> str:
    """Summarize the notes."""
    return f'Write a {style} summary of my notes:\n' + '\n'.join(notes)


plugin('AllowedHosts')
any('/mcp', server.to_action())

# The requests of Pyjo.MCP.Client, to the application of the script, without a server
t = Pyjo.MCP.Test.new()

with subtest('Tools'):
    t.list_tools_ok().status_is(200).tool_exists('add_note').tool_is('delete_note', '/inputSchema/required', ['number'])
    t.call_ok('add_note', text='Call the plumber').status_is(200).structured_content_is(2).is_error_is(False)
    t.call_ok('delete_note', number=1).text_content_is('Deleted "Buy milk"')

# An error of the tool, and invalid arguments, are results, and an unknown tool an error of the protocol
with subtest('Errors'):
    t.call_ok('delete_note', number=9).status_is(200).is_error_is(True).text_content_is('No note 9')
    t.call_ok('delete_note', number='one').is_error_is(True).text_content_like(r'/number: Expected integer')
    t.call_ok('rename_note').status_is(200).error_code_is(-32602).error_message_is('Unknown tool: rename_note')

with subtest('Prompts'):
    t.get_prompt_ok('summarize', style='detailed').status_is(200)
    t.result_is('/messages/0/content/text', 'Write a detailed summary of my notes:\nCall the plumber')
    # The values of the enum of an argument complete it
    t.complete_ok({'type': 'ref/prompt', 'name': 'summarize'}, 'style', 'd').status_is(200)
    t.result_is('/completion/values', ['detailed'])

# A request of another host, as of DNS rebinding
with subtest('Hosts'):
    t.list_tools_ok(headers={'Host': 'evil.example'}).status_is(421)

done_testing()
