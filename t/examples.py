from Pyjo.File import curfile
from Pyjo.Test import *


# The examples of the page are not run, as most of them need a cloud or another server, but each one is Python
EXAMPLES = curfile().dirname().sibling('site', 'examples')

for path in EXAMPLES.list_tree().grep(lambda path: path.extname == 'py'):
    name = path.to_rel(EXAMPLES).to_str()
    try:
        compile(path.slurp('UTF-8'), name, 'exec')
        ok(True, name)
    except SyntaxError as e:
        ok(False, name)
        diag(str(e))

done_testing()
