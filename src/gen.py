# PigletC

from .raddsl_rewrite import *
from .term import *

X, Y = let(X=any), let(Y=any)

rules = alt(
    rule(Push(Int(X)), to(lambda v: "PUSHI %d" % v.X)),
    rule(Load(), to(lambda v: "LOAD")),
    rule(Store(), to(lambda v: "STORE")),
    rule(Call(), to(lambda v: "CALL")),
    rule(Bop("+"), to(lambda v: "ADD")),
    rule(Bop("-"), to(lambda v: "SUB")),
    rule(Bop("*"), to(lambda v: "MUL")),
    rule(Bop("/"), to(lambda v: "DIV")),
    rule(Bop("<"), to(lambda v: "LESS")),
    rule(Bop(">"), to(lambda v: "GREATER")),
    rule(Bop("<="), to(lambda v: "LESS_OR_EQUAL")),
    rule(Bop(">="), to(lambda v: "GREATER_OR_EQUAL")),
    rule(Bop("=="), to(lambda v: "EQUAL")),
    rule(Bop("!="), to(lambda v: "EQUAL\nPUSHI 0\nEQUAL")),
    rule(Label(X), to(lambda v: "L%d:" % v.X)),
    rule(Jump(X), to(lambda v: "JUMP L%d" % v.X)),
    rule(JumpIf0(X), to(lambda v: "JUMP_IF_FALSE L%d" % v.X)),
    rule(Asm(X), to(lambda v: v.X))
)

gen = many(rules)
