# -----------------------------------------------
# Alpha-Beta Pruning Code for the Given Tree
# -----------------------------------------------

import math

# Tree structure exactly matching the problem diagram

tree = {
    "A": ["B", "C"],          # MAX
    "B": ["D", "E"],          # MIN
    "C": ["F", "G"],          # MIN

    "D": ["H", "I"],          # MAX
    "E": ["J", "K"],          # MAX
    "F": ["L", "M"],          # MAX
    "G": ["N", "O"],          # MAX

    # Leaf nodes with values
    "H": [10, 11],
    "I": [9, 12],
    "J": [14, 15],
    "K": [13, 14],
    "L": [5, 2],
    "M": [4, 1],
    "N": [3, 22],
    "O": [20, 21]
}

# Leaf values dictionary
leaf_values = {
    10:10, 11:11, 9:9, 12:12,
    14:14, 15:15, 13:13, 14:14,
    5:5, 2:2, 4:4, 1:1,
    3:3, 22:22, 20:20, 21:21
}

visited = []
pruned = []

# ----------------------------------------------------
# Alpha-Beta functions
# ----------------------------------------------------

def is_leaf(node):
    return isinstance(node, int)

def alphabeta(node, alpha, beta, maximizing):
    visited.append(node)

    # Leaf node
    if is_leaf(node):
        return node

    children = tree[node]

    if maximizing:
        value = -math.inf
        best_child = None
        for child in children:
            if isinstance(child, str):
                child_value = alphabeta(child, alpha, beta, False)
            else:
                child_value = child

            if child_value > value:
                value = child_value
                best_child = child

            alpha = max(alpha, value)

            if beta <= alpha:
                pruned.append((node, "pruned at child", child))
                break

        return value

    else:   # minimizing
        value = math.inf
        best_child = None
        for child in children:
            if isinstance(child, str):
                child_value = alphabeta(child, alpha, beta, True)
            else:
                child_value = child

            if child_value < value:
                value = child_value
                best_child = child

            beta = min(beta, value)

            if beta <= alpha:
                pruned.append((node, "pruned at child", child))
                break

        return value


# ----------------------------------------------------
# Run the algorithm
# ----------------------------------------------------
value_at_root = alphabeta("A", -math.inf, math.inf, True)

print("\n========= RESULT =========")
print("Value of root (A):", value_at_root)

print("\nNodes visited (in order):")
print(visited)

print("\nPruned branches:")
for p in pruned:
    print(p)

'''

========= RESULT =========
Value of root (A): 10

Nodes visited (in order):
['A', 'B', 'D', 'H', 'I', 'E', 'J', 'C', 'F', 'L', 'M']

Pruned branches:
('I', 'pruned at child', 9)
('E', 'pruned at child', 'J')
('L', 'pruned at child', 5)
('M', 'pruned at child', 4)
('C', 'pruned at child', 'F')


'''
