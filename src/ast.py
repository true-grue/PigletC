# PigletC
# Author: Peter Sovietov

from raddsl.parse import *
from .term import *

def pos(state):
  state.out.append(state.pos)
  return True

ident = to(2, lambda p, x: Id(x, pos=p))
integer = to(2, lambda p, x: Int(int(x), pos=p))
op = to(2, lambda p, x: Op(x, pos=p))
bop = to(3, lambda x, o, y: Bop(o[1], x, y, pos=attr(o, "pos")))
assign = to(2, lambda x, y: Assign(x, y, pos=attr(x, "pos")))
call = to(2, lambda x, y: Call(x, y, pos=attr(x, "pos")))
if_st = to(2, lambda x, y: If(x, y, pos=attr(x, "pos")))
while_st = to(2, lambda x, y: While(x, y, pos=attr(x, "pos")))
var = to(1, lambda x: Var(x, pos=attr(x, "pos")))
func = to(2, lambda x, y: Func(x, y, pos=attr(x, "pos")))
