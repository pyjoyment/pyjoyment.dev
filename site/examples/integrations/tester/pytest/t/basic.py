import Pyjo.Test.Pyjo

from Pyjo.File import curfile
from Pyjo.Test import *


# A test script of pyjo-prove, which pytest runs too, as a test of its own
t = Pyjo.Test.Pyjo.new(curfile().dirname().sibling('app.py'))
t.get_ok('/hello/Sara').status_is(200).json_is('/hello', 'Sara')

done_testing()
