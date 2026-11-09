# The dependencies in the inline metadata of the script, which uv installs into an environment of its own, as it runs it
uv add --script app.py Pyjoyment
uv run app.py daemon
./app.py get /

# Another Python, without a virtualenv to make or activate
uv run --python 3.14 app.py get /

# The versions of the dependencies, pinned in app.py.lock next to the script
uv lock --script app.py

# The commands of Pyjoyment, without installing it
uvx --from Pyjoyment pyjo version
uv run --with Pyjoyment pyjo-prove -l -r t

# A project of uv, once the script grows, with its pyproject.toml
uv run app.py generate pyproject
