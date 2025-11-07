# Unification in First Order Logic (Robinson’s Algorithm)
# -------------------------------------------------------
# Supports:
#   - Variables: lowercase identifiers (x, y, z)
#   - Constants: uppercase identifiers (John, Apple)
#   - Functions: f(a, g(x)), Knows(John, x), etc.

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Union

# --- Term model ---
@dataclass(frozen=True)
class Var:
    name: str
    def __repr__(self): return self.name

@dataclass(frozen=True)
class Const:
    name: str
    def __repr__(self): return self.name

@dataclass(frozen=True)
class Func:
    name: str
    args: Tuple['Term', ...]
    def __repr__(self): return f"{self.name}({', '.join(map(repr, self.args))})"

Term = Union[Var, Const, Func]

# --- Tokenizer ---
_token_re = re.compile(r'\s*([A-Za-z_][A-Za-z0-9_]*|\(|\)|,)\s*')

def tokenize(s: str):
    pos = 0
    while pos < len(s):
        m = _token_re.match(s, pos)
        if not m:
            raise ValueError(f"Unexpected character at position {pos}: {s[pos:pos+10]!r}")
        tok = m.group(1)
        yield tok
        pos = m.end()

# --- Parser ---
def parse_term(s: str) -> Term:
    tokens = list(tokenize(s))
    idx = 0

    def next_tok():
        nonlocal idx
        return tokens[idx] if idx < len(tokens) else None

    def consume(expected=None):
        nonlocal idx
        t = next_tok()
        if expected and t != expected:
            raise ValueError(f"Expected {expected!r} but got {t!r}")
        idx += 1
        return t

    def parse_atom() -> Term:
        t = next_tok()
        if t is None:
            raise ValueError("Unexpected end")
        consume(t)
        name = t
        if next_tok() == '(':
            consume('(')
            args = []
            if next_tok() != ')':
                while True:
                    args.append(parse_atom())
                    if next_tok() == ',':
                        consume(',')
                        continue
                    break
            consume(')')
            return Func(name, tuple(args))
        else:
            if name[0].islower():
                return Var(name)
            else:
                return Const(name)

    term = parse_atom()
    if next_tok() is not None:
        raise ValueError("Extra tokens after parsing")
    return term

# --- Substitution and helpers ---
Subst = Dict[str, Term]

def apply_subst(term: Term, subst: Subst) -> Term:
    if isinstance(term, Var):
        if term.name in subst:
            return apply_subst(subst[term.name], subst)
        return term
    if isinstance(term, Const):
        return term
    if isinstance(term, Func):
        return Func(term.name, tuple(apply_subst(a, subst) for a in term.args))
    raise TypeError("Unknown term type")

def occurs_check(var: Var, term: Term, subst: Subst) -> bool:
    term = apply_subst(term, subst)
    if isinstance(term, Var):
        return var.name == term.name
    if isinstance(term, Func):
        return any(occurs_check(var, a, subst) for a in term.args)
    return False

def compose_subst(s1: Subst, s2: Subst) -> Subst:
    new = {v: apply_subst(t, s1) for v, t in s2.items()}
    new.update(s1)
    return new

# --- Unification Algorithm ---
def unify(t1: Term, t2: Term, subst: Optional[Subst]=None) -> Optional[Subst]:
    if subst is None:
        subst = {}
    pairs = [(t1, t2)]
    s = dict(subst)
    while pairs:
        a, b = pairs.pop()
        a = apply_subst(a, s)
        b = apply_subst(b, s)
        if repr(a) == repr(b):
            continue
        if isinstance(a, Var):
            if occurs_check(a, b, s):
                return None
            s = compose_subst({a.name: b}, s)
            continue
        if isinstance(b, Var):
            if occurs_check(b, a, s):
                return None
            s = compose_subst({b.name: a}, s)
            continue
        if isinstance(a, Const) and isinstance(b, Const):
            if a.name != b.name:
                return None
            continue
        if isinstance(a, Func) and isinstance(b, Func):
            if a.name != b.name or len(a.args) != len(b.args):
                return None
            pairs.extend(zip(a.args, b.args))
            continue
        return None
    return s

# --- Helper for output ---
def format_subst(subst: Optional[Subst]) -> str:
    if subst is None:
        return "FAIL (no unifier)"
    if not subst:
        return "{} (empty substitution)"
    items = [f"{v} -> {repr(apply_subst(t, subst))}" for v, t in subst.items()]
    return "{" + ", ".join(items) + "}"

# --- Example Runs ---
examples = [
    ("Eats(x, Apple)", "Eats(Riya, y)"),
    ("p(f(a), g(Y))", "p(X, X)"),
    ("Knows(John, x)", "Knows(x, Elisabeth)"),
    ("f(x, g(y))", "f(g(z), g(a))"),
    ("P(x, h(y))", "P(a, f(z))"),
    ("Ancestor(x, Father(x))", "Ancestor(Father(John), y)"),
    ("f(x,x)", "f(a,b)"),
    ("Knows(x, x)", "Knows(John, y)")
]

print("Unification Examples:\n")
for a_str, b_str in examples:
    A = parse_term(a_str)
    B = parse_term(b_str)
    subst = unify(A, B)
    print(f"{a_str}  =?=  {b_str}\n  => {format_subst(subst)}\n")



'''
Unification Examples:

Eats(x, Apple)  =?=  Eats(Riya, y)
  => {y -> Apple, x -> Riya}

p(f(a), g(Y))  =?=  p(X, X)
  => FAIL (no unifier)

Knows(John, x)  =?=  Knows(x, Elisabeth)
  => FAIL (no unifier)

f(x, g(y))  =?=  f(g(z), g(a))
  => {y -> a, x -> g(z)}

P(x, h(y))  =?=  P(a, f(z))
  => FAIL (no unifier)

Ancestor(x, Father(x))  =?=  Ancestor(Father(John), y)
  => {y -> Father(Father(John)), x -> Father(John)}

f(x,x)  =?=  f(a,b)
  => {x -> a, b -> a}

Knows(x, x)  =?=  Knows(John, y)
  => {x -> John, y -> John}
'''
