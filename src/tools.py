# PigletC
# Author: Peter Sovietov

import sys
from raddsl.rewrite import *
from .term import *

def get_pos(src, pos, offs=0):
  line = src.count("\n", offs, pos)
  line_begin = src.rfind("\n", 0, pos) + 1
  line_end = src.find("\n", line_begin)
  if line_end == -1:
    line_end = len(src)
  col = pos - line_begin
  return line, col, src[line_begin:line_end].replace("\t", " ")

def error(msg, path=None, src=None, pos=None):
  if pos:
    line, col, part = get_pos(src, pos)
    print("%s:%d:%d: %s\n%s" % (path, line + 1, col + 1, msg, part))
    print(" " * col + "^")
  else:
    print(msg)
  sys.exit(1)

is_term = lambda x: type(x) == tuple
is_list = lambda x: type(x) == list
attr = lambda t, a: t[0][a]

def apply_rule(rule, node, **kw):
  t = Tree(node)
  for k in kw:
    setattr(t, k, kw[k])
  if not perform(t, rule):
    error("unsupported term")
  return t.out

X, Y = let(X=id), let(Y=id)

def flatten_term(node):
  if is_term(node):
    map(flatten_term, node)
  elif is_list(node):
    lst = []
    for x in node:
      y = flatten_term(x)
      lst.extend(y if is_list(x) else [y])
    node[:] = lst
  return node

flatten = build(lambda t: flatten_term(t.out))
