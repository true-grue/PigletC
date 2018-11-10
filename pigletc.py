# PigletC, a tiny C-like language compiler for PigletVM,
# see https://github.com/vkazanov/bytecode-interpreters-post
# Author: Peter Sovietov

import os
import sys
from src.main import compile

if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
  path = sys.argv[1]
  with open(path) as f:
    src = f.read()
  c = compile(path, src)
  with open("%s.pvm" % path, "w") as f:
    f.write(c.asm)
else:
  print("usage: pigletc.py file.c")
