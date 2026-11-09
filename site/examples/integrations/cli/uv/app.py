#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["Pyjoyment"]
# ///
from Pyjoyment.Lite import *

import sys


@get('/')
def index(c):
    c.render(json={'python': sys.version.split()[0]})


app.start()
