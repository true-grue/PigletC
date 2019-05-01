# PigletC

from .parse import parse
from .trans import trans
from .gen import gen
from .tools import error, apply


class Compiler:
    def __init__(self, path, text):
        self.path = path
        self.text = text
        self.table = {}
        self.data_cnt = 0
        self.label_cnt = 0
        self.ir = []
        self.asm = ""


def compile(path, text):
    c = Compiler(path, text)
    ast = parse(text, lambda p: error(c, "syntax error", p))
    apply(trans, ast, c=c)
    c.asm = "\n".join(apply(gen, c.ir, c=c) + ["DONE", ""])
    return c
