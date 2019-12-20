# PigletC

from .raddsl_rewrite import *
from .term import *
from .tools import flatten, error


def add_var(X):
    def walk(t):
        t.c.table[X] = dict(ast=t.out, offs=t.c.data_cnt)
        t.c.data_cnt += 1
        return True
    return walk


def add_func(X, Y):
    def walk(t):
        t.c.table[X] = dict(ast=t.out, offs=len(t.c.ir))
        t.c.ir.extend(flatten(Y))
        return True
    return walk


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
    rule(let(X=seq(Id(any), offs("Var"))), to(lambda e: [Push(e.X), Load()])),
    rule(let(X=Int(any)), to(lambda e: [Push(e.X)])),
    rule(Bop(let(O=any), let(X=expr), let(Y=expr)),
         to(lambda e: [e.X, e.Y, Bop(e.O)]))
)

assign_st = rule(
    Assign(let(X=expr), let(Y=expr)), to(lambda e: [e.X[:-1], e.Y, Store()])
)

if_st = rule(
    If(let(X=expr), let(Y=block)), let(L1=label),
    to(lambda e: [e.X, JumpIf0(e.L1), e.Y, Label(e.L1)])
)

while_st = rule(
    While(let(X=expr), let(Y=block)),
    let(L1=label), let(L2=label), to(lambda e: [
        Label(e.L1),
        e.X,
        JumpIf0(e.L2),
        e.Y,
        Jump(e.L1),
        Label(e.L2)
    ])
)

call_st = alt(
    rule(Call(Id("print"), [let(X=expr)]), to(lambda e: [e.X, Asm("PRINT")])),
    rule(Call(let(X=seq(Id(any), offs("Func"))), []),
         to(lambda e: [Call(e.X)]))
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
    rule(Var(Id(let(X=any))), env(lambda e: add_var(e.X))),
    rule(Func(Id(let(X=any)), let(Y=block)), env(lambda e: add_func(e.X, e.Y)))
))
