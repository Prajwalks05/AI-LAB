import itertools
import pandas as pd

# --- Function to evaluate a logical expression ---
def evaluate(expr, model):
    local_dict = {symbol: model[symbol] for symbol in model}
    try:
        return eval(expr, {}, local_dict)
    except Exception as e:
        print(f"Error evaluating '{expr}' with {model}: {e}")
        return False

# --- Function for Truth Table Entailment ---
def truth_table_entailment(kb, query, symbols):
    rows = []
    entails = True

    # Generate combinations: from all False → all True
    for values in itertools.product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        kb_values = [evaluate(stmt, model) for stmt in kb]
        kb_true = all(kb_values)
        query_val = evaluate(query, model)

        row = {sym: model[sym] for sym in symbols}
        for i, stmt in enumerate(kb):
            row[f"KB{i+1}"] = kb_values[i]
        row["KB True?"] = kb_true
        row["Query"] = query_val
        rows.append(row)

        if kb_true and not query_val:
            entails = False

    df = pd.DataFrame(rows)
    return entails, df

# --- User Input ---
print("=== Propositional Logic Entailment Checker ===")
symbols = input("Enter symbols (separated by spaces): ").split()

n = int(input("Enter number of KB statements: "))
kb = []
print("Enter KB statements (use 'not', 'and', 'or', parentheses):")
for i in range(n):
    kb.append(input(f"KB{i+1}: "))

query = input("Enter the query statement: ")

# --- Run Entailment Check ---
entails, truth_table = truth_table_entailment(kb, query, symbols)

# Sort truth table from False False False → True True True
truth_table = truth_table.sort_values(by=symbols, ascending=True, ignore_index=True)

# --- Output ---
print("\nKnowledge Base:")
for i, s in enumerate(kb, 1):
    print(f"  {i}. {s}")

print("\nQuery:", query)
print("\n--- Truth Table ---")
print(truth_table.to_string(index=False))

print("\nResult:")
print("✅ The query IS ENTAILED by the Knowledge Base."
      if entails else "❌ The query is NOT entailed by the Knowledge Base.")


'''
Question1:


=== Propositional Logic Entailment Checker ===
Enter symbols (separated by spaces): A B C
Enter number of KB statements: 1
Enter KB statements (use 'not', 'and', 'or', parentheses):
KB1: (A or C) and (B or not C)
Enter the query statement: A or B

Knowledge Base:
  1. (A or C) and (B or not C)

Query: A or B

--- Truth Table ---
    A     B     C   KB1  KB True?  Query
False False False False     False  False
False False  True False     False  False
False  True False False     False   True
False  True  True  True      True   True
 True False False  True      True   True
 True False  True False     False   True
 True  True False  True      True   True
 True  True  True  True      True   True

Result:
✅ The query IS ENTAILED by the Knowledge Base.


Question2:


=== Propositional Logic Entailment Checker ===
Enter symbols (separated by spaces): P Q R
Enter number of KB statements: 3
Enter KB statements (use 'not', 'and', 'or', parentheses):
KB1: R
KB2: not R or P
KB3: not Q or P
Enter the query statement: Q or R

Knowledge Base:
  1. R
  2. not R or P
  3. not Q or P

Query: Q or R

--- Truth Table ---
    P     Q     R   KB1   KB2   KB3  KB True?  Query
False False False False  True  True     False  False
False False  True  True False  True     False   True
False  True False False  True False     False   True
False  True  True  True False False     False   True
 True False False False  True  True     False  False
 True False  True  True  True  True      True   True
 True  True False False  True  True     False   True
 True  True  True  True  True  True      True   True

Result:
✅ The query IS ENTAILED by the Knowledge Base.

=== Code Execution Successful ===
'''
