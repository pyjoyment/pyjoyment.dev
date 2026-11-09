import Pyjo.Template

from Pyjo.File import curfile

import sys


if len(sys.argv) < 3:
    sys.exit('Usage: render.py SERVER_NAME UPSTREAM...')

# A template of any text, without the escaping of HTML, whose values are its variables
template = Pyjo.Template.new(vars=True)
output = template.render_file(
    curfile().sibling('site.conf.ep'), {'server_name': sys.argv[1], 'upstreams': sys.argv[2:]}
)

# A Pyjo.Exception with the line of the template, instead of the text, when it fails
if isinstance(output, Exception):
    sys.exit(str(output))
print(output, end='')
