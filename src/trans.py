# PigletC

from .raddsl_rewrite import *
from .term import *
from .tools import flatten, error


@scoped
def add_var(t, X):
    t.c.table[X] = dict(ast=t.out, offs=t.c.data_cnt)
    t.c.data_cnt += 1
    return True


@scoped
def add_func(t, X, Y):
    t.c.table[X] = dict(ast=t.out, offs=len(t.c.ir))
    t.c.ir.extend(flatten(Y))
    return True


def label(t):
    t.out = t.c.label_cnt
    t.c.label_cnt += 1
    return True


def offs(tag):
    def walk(t):
        entry = t.c.table.get(t.out[1])
        if not entry or attr(entry["ast"], "tag") != tag:
            error(t.c, "unknown name '%s'" % t.out[1], attr(t.out, "pos"))
        t.out = Int(entry["offs"])
        return True
    return walk


expr = delay(lambda: expr)
block = delay(lambda: block)

expr = alt(
    rule(let(X=seq(Id(any), offs("Var"))), to(lambda v: [Push(v.X), Load()])),
    rule(let(X=Int(any)), to(lambda v: [Push(v.X)])),
    rule(Bop(let(O=any), let(X=expr), let(Y=expr)),
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
    rule(Call(let(X=seq(Id(any), offs("Func"))), []),
         to(lambda v: [Call(v.X)]))
)

stmt = alt(
    assign_st,
    if_st,
    while_st,
    call_st,
    block
)

block = many(stmt)

trans = many(alt(
    rule(Var(Id(let(X=any))), add_var),
    rule(Func(Id(let(X=any)), let(Y=block)), add_func),
))
