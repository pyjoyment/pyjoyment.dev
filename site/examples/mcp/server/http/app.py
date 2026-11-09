import Pyjo.JSON.RPC

from Pyjo.MCP.Server import Server
from Pyjo.MCP.Tool import Error
from Pyjoyment.Lite import *

from typing import Literal, TypedDict


class Note(TypedDict):
    number: int
    text: str


class Found(TypedDict):
    notes: list[Note]


server = Server(name='notes', version='1.0.0', instructions='The notes of the user, which the model adds and finds.')
notes = ['Buy milk', 'Call the plumber']


# The schemas of the tool come from its type hints, and its descriptions from its docstring
@server.tool
def add_note(text: str) -> Note:
    """Add a note.

    :param text: The text of the note.
    """
    notes.append(text)
    return Note(number=len(notes), text=text)


@server.tool(annotations={'readOnlyHint': True})
def find_notes(word: str) -> Found:
    """Find the notes with a word, in any case.

    :param word: The word to look for.
    """
    found = [Note(number=i, text=text) for i, text in enumerate(notes, 1) if word.lower() in text.lower()]
    if not found:
        # A result with isError, which the model reads to try again
        raise Error.new(f'No note with "{word}"')
    return Found(notes=found)


# A resource template, of the URIs that a client reads
@server.resource('notes://{number}', mime_type='text/plain')
def note(number: str) -> str:
    """A note, by its number."""
    if not number.isdigit() or not 0 < int(number) <= len(notes):
        raise Pyjo.JSON.RPC.Error.new(Pyjo.JSON.RPC.INVALID_PARAMS, 'Resource not found', {'uri': f'notes://{number}'})
    return notes[int(number) - 1]


# The values of the enum complete the argument of the prompt
@server.prompt
def summarize(style: Literal['short', 'detailed'] = 'short') -> str:
    """Summarize the notes."""
    return f'Write a {style} summary of my notes:\n' + '\n'.join(notes)


# Host and Origin of localhost only, against DNS rebinding
plugin('AllowedHosts')

any('/mcp', server.to_action())

app.start()
