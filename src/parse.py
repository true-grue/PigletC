# PigletC

from .raddsl_parse import *
from .term import *


def mark(s):
    s.out.append(s.pos)
    return True


def ast_ident(kw):
    return to(2,
              lambda p, x: Op(x, pos=p) if x in kw else Id(x, pos=p))


ast_integer = to(2, lambda p, x: Int(int(x), pos=p))
ast_op = to(2, lambda p, x: Op(x, pos=p))
ast_bop = to(3, lambda x, o, y: Bop(o[1], x, y, pos=attr(o, "pos")))
ast_assign = to(2, lambda x, y: Assign(x, y, pos=attr(x, "pos")))
ast_call = to(2, lambda x, y: Call(x, y, pos=attr(x, "pos")))
ast_if = to(2, lambda x, y: If(x, y, pos=attr(x, "pos")))
ast_while = to(2, lambda x, y: While(x, y, pos=attr(x, "pos")))
ast_var = to(1, lambda x: Var(x, pos=attr(x, "pos")))
ast_func = to(2, lambda x, y: Func(x, y, pos=attr(x, "pos")))

OPERATORS = "; ( ) { } + -  * / = != < <= > >= ==".split()
KEYWORDS = "if while int void".split()
single_comment = seq(a("//"), many(non(a("\n"))))
multi_comment = seq(a("/*"), many(non(a("*/"))), a("*/"))
comment = alt(single_comment, multi_comment)
ws = many(alt(space, comment))
name = seq(cite(letter, many(alt(letter, digit))), ast_ident(KEYWORDS))
integer = seq(cite(some(digit)), ast_integer)
operator = seq(cite(match(OPERATORS)), ast_op)
token = memo(seq(ws, mark, alt(operator, name, integer)))
ident = seq(token, guard(lambda x: x[0] == "Id"))


def op(o): return seq(token, guard(lambda x: x == ("Op", o)), drop)


def left(p): return seq(tab.expr(p + 1), ast_bop)


def block(x): return block(x)


tab = Prec(token, lambda x: x[1] if x[0] == "Op" else attr(x, "tag"))
tab.prefix["Id"] = empty
tab.prefix["Int"] = empty
tab.prefix["("] = seq(drop, tab.expr(0), op(")"))
tab.infix["!="] = left, 1
tab.infix["=="] = left, 1
tab.infix["<="] = left, 2
tab.infix[">="] = left, 2
tab.infix["<"] = left, 2
tab.infix[">"] = left, 2
tab.infix["+"] = left, 3
tab.infix["-"] = left, 3
tab.infix["*"] = left, 4
tab.infix["/"] = left, 4

assign = seq(ident, op("="), tab.expr(0), ast_assign)
args = group(opt(list_of(tab.expr(0), op(","))))
call = seq(ident, op("("), args, op(")"), ast_call)
if_st = seq(op("if"), tab.expr(0), block, ast_if)
while_st = seq(op("while"), tab.expr(0), block, ast_while)
stmt = alt(seq(alt(assign, call), op(";")), if_st, while_st)
block = seq(op("{"), group(many(stmt)), op("}"))
var_def = seq(op("int"), ident, op(";"), ast_var)
func_def = seq(op("void"), ident, op("("), op(")"), block, ast_func)
main = seq(many(alt(var_def, func_def)), ws, end)


def parse(text, error):
    s = Stream(text)
    return s.out if main(s) else error(s.epos)
