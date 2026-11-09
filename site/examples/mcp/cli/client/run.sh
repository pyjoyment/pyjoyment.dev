# The tools of the server of MCP over HTTP
python mcp_call.py
# add_note    Add a note.
# find_notes  Find the notes with a word, in any case.

python mcp_call.py find_notes word=milk
# {"notes":[{"number":1,"text":"Buy milk"}]}

# An error of the tool, for the exit status
python mcp_call.py find_notes word=eggs || echo "Failed with $?"
# No note with "eggs"
# Failed with 1

# Numbers as JSON, of another server
export MCP_URL=http://127.0.0.1:3001/mcp
python mcp_call.py divide a:=7 b:=2
# 3.5
