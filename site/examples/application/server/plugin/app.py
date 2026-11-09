from Pyjoyment.Lite import *


# MyPlugins/Timing.py next to the script, by its dotted name
plugin('MyPlugins.Timing', {'name': 'hello'})


@get('/')
def index(c):
    c.render(text=f'Hello after {c.timing.elapsed() * 1000:.3f} ms')


app.start()
