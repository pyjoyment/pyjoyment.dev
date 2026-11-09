python app.py daemon -l http://127.0.0.1:3000 &

# The endpoint of Streamable HTTP, stateless: no session, as each request carries its revision and the capabilities of
# its client in _meta, and the headers of MCP that match its body
curl http://127.0.0.1:3000/mcp \
  -H 'MCP-Protocol-Version: 2026-07-28' -H 'Mcp-Method: tools/call' -H 'Mcp-Name: find_notes' \
  --json '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
    "name": "find_notes", "arguments": {"word": "milk"},
    "_meta": {"io.modelcontextprotocol/protocolVersion": "2026-07-28", "io.modelcontextprotocol/clientCapabilities": {}}
  }}'
# {"jsonrpc":"2.0","result":{"resultType":"complete","content":[...],
#  "structuredContent":{"notes":[{"number":1,"text":"Buy milk"}]},"isError":false,...},"id":1}

# Another host, as of DNS rebinding
curl -i -H 'Host: evil.example' http://127.0.0.1:3000/mcp
# HTTP/1.1 421 Misdirected Request
