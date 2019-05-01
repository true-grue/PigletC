# PigletC

import sys
from .raddsl_rewrite import Tree, perform
from .term import is_term, is_list


def error(c, msg, pos=None):
    if pos is None:
        print(msg)
    else:
        line = c.text.count("\n", 0, pos)
        col = pos - (c.text.rfind("\n", 0, pos) + 1)
        print("%s:%d:%d: %s" % (c.path, line + 1, col + 1, msg))
    sys.exit(1)


def apply(rules, ast, **attrs):
    t = Tree(ast)
    for a in attrs:
        setattr(t, a, attrs[a])
    if not perform(t, rules):
        print("apply error")
        sys.exit(1)
    return t.out


def flatten(ast):
    if is_term(ast):
        map(flatten, ast)
    elif is_list(ast):
        lst = []
        for x in ast:
            y = flatten(x)
            lst.extend(y if is_list(x) else [y])
        ast[:] = lst
    return ast
