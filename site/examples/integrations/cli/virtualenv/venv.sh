python3 -m venv .venv
.venv/bin/pip install Pyjoyment

# The Python of the virtualenv runs the script, and its commands are in .venv/bin
.venv/bin/python app.py get /   # {"python":"\/srv\/myapp\/.venv\/bin\/python"}
.venv/bin/pyjo version
.venv/bin/pyjo-prove -l -r t

# Activated, its Python is the python of the shebang of the script
. .venv/bin/activate
./app.py daemon
pyjo-reload app.py
deactivate

# The same packages elsewhere, as pip freeze pins them
.venv/bin/pip freeze > requirements.txt
