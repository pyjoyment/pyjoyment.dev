# A message of JSON-RPC on each line of the standard input, and its response on a line of the standard output, until
# the end of the input
jq -c . <<'EOF' | python app.py stdio
{
  "jsonrpc": "2.0", "id": 1, "method": "tools/call",
  "params": {
    "name": "find_todos", "arguments": {"extension": "py"},
    "_meta": {"io.modelcontextprotocol/protocolVersion": "2026-07-28", "io.modelcontextprotocol/clientCapabilities": {}}
  }
}
EOF
# [2026-11-09 17:38:49.49951] [75606] [info] 2 TODO comments in *.py
# {"jsonrpc":"2.0","result":{"resultType":"complete","content":[...],"structuredContent":{"todos":[
#  {"file":"lib\/util.py","line":1,"text":"# TODO: tests"},{"file":"main.py","line":1,"text":"x = 1  # TODO: rename"}
#  ]},"isError":false,...},"id":1}

# The same tools over Streamable HTTP
python app.py daemon -l http://127.0.0.1:3000
