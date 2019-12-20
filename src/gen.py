# PigletC

from .raddsl_rewrite import *
from .term import *

X, Y = let(X=any), let(Y=any)

rules = rule(alt(
    seq(Push(Int(X)), to(lambda e: "PUSHI %d" % e.X)),
    seq(Load(), to(lambda e: "LOAD")),
    seq(Store(), to(lambda e: "STORE")),
    seq(Call(), to(lambda e: "CALL")),
    seq(Bop("+"), to(lambda e: "ADD")),
    seq(Bop("-"), to(lambda e: "SUB")),
    seq(Bop("*"), to(lambda e: "MUL")),
    seq(Bop("/"), to(lambda e: "DIV")),
    seq(Bop("<"), to(lambda e: "LESS")),
    seq(Bop(">"), to(lambda e: "GREATER")),
    seq(Bop("<="), to(lambda e: "LESS_OR_EQUAL")),
    seq(Bop(">="), to(lambda e: "GREATER_OR_EQUAL")),
    seq(Bop("=="), to(lambda e: "EQUAL")),
    seq(Bop("!="), to(lambda e: "EQUAL\nPUSHI 0\nEQUAL")),
    seq(Label(X), to(lambda e: "L%d:" % e.X)),
    seq(Jump(X), to(lambda e: "JUMP L%d" % e.X)),
    seq(JumpIf0(X), to(lambda e: "JUMP_IF_FALSE L%d" % e.X)),
    seq(Asm(X), to(lambda e: e.X))
))

gen = many(rules)
