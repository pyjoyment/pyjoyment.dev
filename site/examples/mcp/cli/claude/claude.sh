# A server over HTTP, which runs already, as python app.py daemon -l http://127.0.0.1:3000
claude mcp add --transport http notes http://127.0.0.1:3000/mcp

# With a token, in a header of every request
claude mcp add --transport http notes https://notes.example.com/mcp --header 'Authorization: Bearer sesame'

# A server over stdio, which Claude Code starts in the directory of the project, with the dependencies of the script
uv add --script app.py Pyjo-MCP
claude mcp add project -- uv run app.py stdio

# For the whole team, in .mcp.json of the project, which Claude Code asks to trust before it starts the server
claude mcp add --scope project project -- uv run app.py stdio

# The servers, whether they connect, and their tools in Claude Code
claude mcp list
/mcp
