# PigletC
# Author: Peter Sovietov

from raddsl.parse import *
from  . import ast

single_comment = seq(a("//"), many(non(a("\n"))))
multi_comment = seq(a("/*"), many(non(a("*/"))), a("*/"))
comment = alt(single_comment, multi_comment)
ws = many(alt(space, comment))
name = seq(quote(letter, many(alt(letter, digit))), ast.ident)
integer = seq(quote(some(digit)), ast.integer)
OPERATORS = "; ( ) { } + -  * / = != < <= > >= if while int void".split()
operator = seq(quote(match(OPERATORS)), ast.op)
tokens = seq(many(seq(ws, ast.pos, alt(operator, name, integer))), ws, end)

ident = push(eat(lambda x: x[0] == "Id"))
op = lambda n: eat(lambda x: x == ast.Op(n))
expr_val = lambda x: x[1] if x[0] == "Op" else ast.attr(x, "tag")
expr = tdop(
  lambda x: prefix.get(expr_val(x)), lambda x: infix.get(expr_val(x))
)
exp = expr(0)
left_op = lambda b: seq(push(id), expr(b + 1), ast.bop)
prefix = {
  "Id": push(id),
  "Int": push(id),
  "(": seq(id, exp, op(")"))
}
infix = {
  "*": (left_op, 40),
  "/": (left_op, 40),
  "+": (left_op, 30),
  "-": (left_op, 30),
  "<": (left_op, 20),
  ">": (left_op, 20),
  "<=": (left_op, 20),
  ">=": (left_op, 20),
  "==": (left_op, 10),
  "!=": (left_op, 10)
}
block = lambda x: block(x)
assign = seq(ident, op("="), exp, ast.assign)
args = group(opt(list_of(exp, op(","))))
call = seq(ident, op("("), args, op(")"), ast.call)
if_st = seq(op("if"), exp, block, ast.if_st)
while_st = seq(op("while"), exp, block, ast.while_st)
stmt = alt(seq(alt(assign, call), op(";")), if_st, while_st)
block = seq(op("{"), group(many(stmt)), op("}"))
var_decl = seq(op("int"), ident, op(";"), ast.var)
func_decl = seq(op("void"), ident, op("("), op(")"), block, ast.func)
decls = seq(group(many(alt(var_decl, func_decl))), end)

def parse(src, error):
  s1 = Stream(src)
  t = s1.out if tokens(s1) else error(s1.error_pos)
  s2 = Stream(t)
  if decls(s2):
    return s2.out[0]
  error(ast.attr(s2.buf[min(s2.error_pos, s2.size - 1)], "pos"))
