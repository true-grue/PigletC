# PigletC, a tiny C-like language compiler for PigletVM,
# see https://github.com/vkazanov/bytecode-interpreters-post
# Author: Peter Sovietov

import sys
from src.main import Compiler, compile

if len(sys.argv) == 2:
  path = sys.argv[1]
  with open(path) as f:
    src = f.read()
  c = Compiler(path, src)
  compile(c)
  with open("%s.pvm" % path, "w") as f:
    f.write(c.asm)
else:
  print("usage: pigletc.py file.c")
