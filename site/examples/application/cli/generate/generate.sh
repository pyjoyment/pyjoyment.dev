# An application in one file, app.py
uvx --from Pyjoyment pyjo generate lite-app app.py
uv add --script app.py Pyjoyment
uv run app.py daemon

# An application with controllers, templates and tests, in my_app/
uvx --from Pyjoyment pyjo generate app MyApp
cd my_app
uv run python -m MyApp daemon
uv run pyjo-prove -l -r t

# The files of its deployment
uv run python -m MyApp generate dockerfile
uv run python -m MyApp generate kubernetes
uv run python -m MyApp generate lambda-zip
