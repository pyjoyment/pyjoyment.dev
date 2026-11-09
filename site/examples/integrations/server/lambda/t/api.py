import Pyjo.Test.Pyjo

from Pyjo.File import curfile
from Pyjo.Test import *


# The function as API Gateway runs it, with the path of the mount as its stage, without AWS
t = Pyjo.Test.Pyjo.new(curfile().dirname().sibling('app.py'))

t.get_ok('/api/hello?name=Sara').status_is(200).json_is('/hello', 'Sara').json_is('/path', '/hello')
t.get_ok('/api/').status_is(200).json_is('/hello', 'World')

done_testing()
