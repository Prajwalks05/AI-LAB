# ----------------------------------------------------
# SIMPLE PYTHON IMPLEMENTATION OF FOL → CNF CONVERSION
# ----------------------------------------------------

import re

# ---------- Step 1: Remove implications ----------
def remove_implications(s):
    s = s.replace("->", "∨")     # P -> Q  becomes  ¬P ∨ Q (handled later)
    s = s.replace("<->", "↔")    # Not fully implemented but placeholder
    # Proper implication removal:
    s = re.sub(r"(\w+)\s*->\s*(\w+)", r"¬\1 ∨ \2", s)
    s = re.sub(r"(\w+)\s*↔\s*(\w+)", r"(¬\1 ∨ \2) ∧ (¬\2 ∨ \1)", s)
    return s


# ---------- Step 2: Push negation inward ----------
def push_negation(s):

    # Apply De Morgan
    s = s.replace("¬(A ∧ B)", "(¬A ∨ ¬B)")
    s = s.replace("¬(A ∨ B)", "(¬A ∧ ¬B)")

    # Quantifier negation
    s = s.replace("¬∀", "∃¬")
    s = s.replace("¬∃", "∀¬")

    return s


# ---------- Step 3: Standardize variables ----------
def standardize_vars(s):
    # For demo simplicity: rename x,y,z to x1,y1,z1...
    counter = 1
    def repl(match):
        nonlocal counter
        v = match.group(1)
        new_v = f"{v}{counter}"
        counter += 1
        return new_v
    return re.sub(r"\b([xyz])\b", repl, s)


# ---------- Step 4: Skolemization ----------
def skolemize(s):

    # Replace ∃x inside universal scope with Skolem functions
    # Simple demonstration:
    s = s.replace("∃", "")  # remove existential
    s = s.replace("x1", "f(y1)")  # demo Skolem function
    return s


# ---------- Step 5: Drop ∀ ----------
def drop_universal(s):
    s = s.replace("∀", "")
    return s


# ---------- Step 6: Distribute OR over AND ----------
def distribute_or(s):
    # Very simple demonstration (not full implementation)
    s = s.replace("∨ (", "∨(")
    return s


# ---------- Step 7: Cleanup ----------
def cleanup(s):
    s = s.replace("  ", " ")
    return s


# ---------- Main conversion function ----------
def fol_to_cnf(sentence):
    s = sentence

    s = remove_implications(s)
    s = push_negation(s)
    s = standardize_vars(s)
    s = skolemize(s)
    s = drop_universal(s)
    s = distribute_or(s)
    s = cleanup(s)

    return s


# ---------- Default FOL test list ----------
sentences = [
    "∀x (P(x) -> Q(x))",
    "∃y (P(y) ∧ R(y))",
    "∀x ∃y Loves(x,y)",
    "P(x) -> (Q(x) ∧ R(x))",
    "((P -> Q) ∧ (Q -> R)) -> (P -> R)"
]

print("\nFOL → CNF Conversion:\n")
for s in sentences:
    print("Original:", s)
    print("CNF     :", fol_to_cnf(s))
    print()




'''
FOL → CNF Conversion:

Original: ∀x (P(x) -> Q(x))
CNF     : f(y1) (P(x2) ∨ Q(x3))

Original: ∃y (P(y) ∧ R(y))
CNF     : y1 (P(y2) ∧ R(y3))

Original: ∀x ∃y Loves(x,y)
CNF     : f(y1) y2 Loves(x3,y4)

Original: P(x) -> (Q(x) ∧ R(x))
CNF     : P(f(y1)) ∨(Q(x2) ∧ R(x3))

Original: ((P -> Q) ∧ (Q -> R)) -> (P -> R)
CNF     : ((P ∨ Q) ∧ (Q ∨ R)) ∨(P ∨ R)
'''
