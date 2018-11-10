# PigletC
# Author: Peter Sovietov

import sys
from .parse import parse
from .tools import *
from .trans import trans
from .gen import gen

class Compiler:
  def __init__(self, path, src):
    self.path = path
    self.src = src
    self.table = {}
    self.data_cnt = 0
    self.label_cnt = 0
    self.ir = []
    self.asm = ""

def compile(path, src):
  c = Compiler(path, src)
  ast = parse(src, lambda p: error("syntax error", path, src, p))
  apply_rule(trans, ast, c=c)
  c.asm = "\n".join(apply_rule(gen, c.ir, c=c) + ["DONE", ""])
  return c
