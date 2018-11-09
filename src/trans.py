# PigletC
# Author: Peter Sovietov

from .tools import *

@act
def add_var(t, X):
  t.c.table[X] = dict(offs=t.c.data_cnt, ast=t.out)
  t.c.data_cnt += 1
  return True

@act
def add_func(t, X):
  t.c.table[X] = dict(ast=t.out)
  return True

def set_func(t):
  t.c.curr_func = t.out
  return True

def check_id(t, tag):
  n = t.out[1]
  if n not in t.c.table or attr(t.c.table[n]["ast"], "tag") != tag:
    error("unknown name", t.c.path, t.c.src, attr(t.out, "pos"))

def var_id(t):
  check_id(t, "Var")
  n = t.out[1]
  t.out = Int(t.c.table[n]["offs"])
  return True

def func_id(t):
  check_id(t, "Func")
  return True

def label(t):
  t.out = t.c.label_cnt
  t.c.label_cnt += 1
  return True

def add_ir(t):
  t.c.ir.extend(t.out)
  return True

expr = delay(lambda: expr)
block = delay(lambda: block)

expr = alt(
  rule(let(X=seq(Id(id), var_id)), to(lambda v: [Push(v.X), Load()])),
  rule(let(X=Int(id)), to(lambda v: [Push(v.X)])),
  rule(Bop(let(O=id), let(X=expr), let(Y=expr)),
    to(lambda v: [v.X, v.Y, Bop(v.O)]))
)

assign_st = rule(
  Assign(let(X=expr), let(Y=expr)), to(lambda v: [v.X[:-1], v.Y, Store()])
)

if_st = rule(
  If(let(X=expr), let(Y=block)), let(L1=label),
    to(lambda v: [v.X, JumpIf0(v.L1), v.Y, Label(v.L1)])
)

while_st = rule(
  While(let(X=expr), let(Y=block)),
  let(L1=label), let(L2=label), to(lambda v: [
    Label(v.L1),
    v.X,
    JumpIf0(v.L2),
    v.Y,
    Jump(v.L1),
    Label(v.L2)
  ])
)

call_st = alt(
  rule(Call(Id("print"), [let(X=expr)]), to(lambda v: [v.X, Asm("PRINT")])),
  rule(Call(seq(X, func_id), []), to(lambda v: [Call(v.X)]))
)

stmt = alt(
  assign_st,
  if_st,
  while_st,
  call_st,
  block
)

block = each(stmt)

add_decls = each(alt(
  rule(Var(Id(X)), add_var),
  rule(Func(Id(X), id), add_func)
))

trans_decls = each(opt(
  Func(Id(set_func), seq(block, flatten, add_ir))
))

trans = seq(add_decls, trans_decls)
