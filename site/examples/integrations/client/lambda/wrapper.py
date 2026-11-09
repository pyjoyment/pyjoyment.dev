#!/usr/bin/env python3
# The wrapper of AWS_LAMBDA_EXEC_WRAPPER, which runs the runtime client of Pyjo.Server.Lambda, which streams, in the place
# of the one of the runtime of Python, which does not, with the handler of _HANDLER
import Pyjo.Server.Lambda


Pyjo.Server.Lambda.main([])
