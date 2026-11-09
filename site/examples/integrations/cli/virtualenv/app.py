#!/usr/bin/env python
from Pyjoyment.Lite import *

import sys


@get('/')
def index(c):
    c.render(json={'python': sys.executable})


app.start()
