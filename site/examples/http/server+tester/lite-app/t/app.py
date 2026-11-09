import Pyjo.Test.Pyjo

from Pyjo.File import curfile
from Pyjo.Test import *


t = Pyjo.Test.Pyjo.new(curfile().dirname().sibling('app.py'))

t.get_ok('/hello').status_is(200).json_is('/hello', 'World')
t.get_ok('/hello/Sara').status_is(200).json_is('/hello', 'Sara')

done_testing()
