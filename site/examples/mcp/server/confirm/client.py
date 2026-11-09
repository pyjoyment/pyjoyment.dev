import Pyjo.MCP.Client

import sys


# The client declares that its user answers the forms of the server
client = Pyjo.MCP.Client.new('http://127.0.0.1:3000/mcp')
client.capabilities = {'elicitation': {}}

arguments = {'name': sys.argv[1]}
result = client.call_tool('delete_file', arguments)
while result['resultType'] == 'input_required':
    responses = {}
    for key, request in result['inputRequests'].items():
        yes = input(f'{request["params"]["message"]} [y/N] ').lower() == 'y'
        responses[key] = {'action': 'accept', 'content': {}} if yes else {'action': 'decline'}
    state = result.get('requestState')
    result = client.call_tool('delete_file', arguments, input_responses=responses, request_state=state)

print(result['content'][0]['text'])
