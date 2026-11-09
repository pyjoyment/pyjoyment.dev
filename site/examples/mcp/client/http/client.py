import Pyjo.JSON.RPC
import Pyjo.MCP.Client
import Pyjo.Promise


client = Pyjo.MCP.Client.new('http://127.0.0.1:3000/mcp', name='notes-client')

# Stateless: no initialize, as each request carries the revision and the capabilities of the client
print(client.discover()['instructions'])
for tool in client.list_tools()['tools']:
    print(f'{tool["name"]}: {tool["description"]}')

number = client.call_tool('add_note', {'text': 'Water the plants'})['structuredContent']['number']
print(client.read_resource(f'notes://{number}')['contents'][0]['text'])

# An error of the tool is a result, which the model reads, and an error of the protocol an exception
result = client.call_tool('find_notes', {'word': 'eggs'})
if result['isError']:
    print(result['content'][0]['text'])
try:
    client.read_resource('notes://99')
except Pyjo.JSON.RPC.Error as e:
    print(f'{e.code} {e.message}: {e.data}')

for message in client.get_prompt('summarize', {'style': 'detailed'})['messages']:
    print(f'{message["role"]}: {message["content"]["text"]}')


def found(*results):
    for (result,) in results:
        print(result['structuredContent'])


# Concurrent calls, with promises
promises = [client.call_tool_p('find_notes', {'word': word}) for word in ('milk', 'plumber', 'plants')]
Pyjo.Promise.all(*promises).then(found).wait()
