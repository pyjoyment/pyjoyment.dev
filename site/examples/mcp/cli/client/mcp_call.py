"""
Usage: python mcp_call.py [OPTIONS] [TOOL [NAME=VALUE | NAME:=JSON ...]]

  python mcp_call.py
  python mcp_call.py find_notes word=milk
  python mcp_call.py -u https://example.com/mcp -H 'Authorization: Bearer sesame' add_note text='Buy bread'

Options:
  -H, --header <header>   Header of every request, as "Name: value"
  -j, --json              Print the JSON of the result
  -u, --url <url>         URL of the endpoint of MCP, defaults to the value of MCP_URL or "http://127.0.0.1:3000/mcp"
"""

import Pyjo.Exception
import Pyjo.JSON
import Pyjo.MCP.Client

from Pyjo.Util import getopt, tablify

import sys


# The options before the name of the tool, as its arguments are not options, and the environment of MCP_URL
headers = []
opts = getopt({'H|header=s': headers, 'j|json': None, 'u|url=s': None}, require_order=True, env_prefix='MCP_')
if not opts:
    sys.exit(__doc__)
client = Pyjo.MCP.Client.new(opts.url or 'http://127.0.0.1:3000/mcp', name='mcp_call')
client.headers = dict((part.strip() for part in header.split(':', 1)) for header in headers)

try:
    if len(sys.argv) < 2:
        tools = client.list_tools()['tools']
        print(tablify([[tool['name'], tool.get('description', '')] for tool in tools]), end='')
        sys.exit()

    # Strings, or JSON after :=, as HTTPie has them
    arguments = {}
    for argument in sys.argv[2:]:
        name, json, value = argument.partition(':=') if ':=' in argument else argument.partition('=')
        arguments[name] = Pyjo.JSON.from_json(value) if json == ':=' else value
    result = client.call_tool(sys.argv[1], arguments)
except Pyjo.Exception.object as e:
    # An error of the protocol or of the connection, and not one of the tool, which is a result
    sys.exit(e.message.strip())

if opts.json:
    print(Pyjo.JSON.to_json(result))
else:
    print('\n'.join(item['text'] for item in result['content'] if item['type'] == 'text'))
sys.exit(1 if result['isError'] else 0)
