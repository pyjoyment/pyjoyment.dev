import Pyjo.App.Lambda

from Pyjo.File import curfile
from Pyjoyment.Lite import *


# The function in a process of its own, which gets its events through the Runtime API of Lambda, one after another, as
# on AWS, with the events of a REST API
function = Pyjo.App.Lambda.new(function='function.handler', task_root=curfile().dirname().to_str(), payload='1.0')
plugin('Mount', {'/api': function})

app.start()
