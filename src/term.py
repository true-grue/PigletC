# PigletC


class Head(dict):
    def __eq__(self, right):
        return self["tag"] == right

    def __ne__(self, right):
        return not self.__eq__(right)

    def __repr__(self):
        return self["tag"]


def make_term(tag):
    return lambda *args, **attrs: (Head(tag=tag, **attrs),) + args


def is_term(x):
    return isinstance(x, tuple)


def is_list(x):
    return isinstance(x, list)


def attr(term, name):
    return term[0][name]


Id = make_term("Id")
Int = make_term("Int")
Op = make_term("Op")
Bop = make_term("Bop")
Assign = make_term("Assign")
Call = make_term("Call")
If = make_term("If")
While = make_term("While")
Var = make_term("Var")
Func = make_term("Func")
Push = make_term("Push")
Load = make_term("Load")
Store = make_term("Store")
Label = make_term("Label")
Jump = make_term("Jump")
JumpIf0 = make_term("JumpIf0")
Asm = make_term("Asm")
