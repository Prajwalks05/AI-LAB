from collections import deque
# Manhattan Distance Heuristic
def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            current_row, current_col = i // 3, i % 3
            goal_index = goal.index(state[i])
            goal_row, goal_col = goal_index // 3, goal_index % 3
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)
    return distance

# Define goal state
goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)  # 0 represents the blank tile

# Helper function to print puzzle in 3x3 grid
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

# Function to find possible moves (neighbors)
def get_neighbors(state):
    neighbors = []
    index = state.index(0)
    row, col = index // 3, index % 3
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

    for dx, dy in moves:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_index = new_row * 3 + new_col
            new_state = list(state)
            # Swap blank with target tile
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append(tuple(new_state))
    return neighbors

# Depth-Limited Search (DLS)
def depth_limited_search(state, goal, depth_limit, path, visited):
    print(f"Exploring state with Manhattan Distance = {manhattan_distance(state, goal)}")
    print_puzzle(state)

    if state == goal:
        return path

    if depth_limit == 0:
        return None

    visited.add(state)

    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            result = depth_limited_search(neighbor, goal, depth_limit - 1, path + [neighbor], visited)
            if result is not None:
                return result

    return None


# Iterative Deepening Search (IDS)
def iterative_deepening_search(start, goal):
    depth = 0
    while True:
        visited = set()
        print(f"🔹 Searching at depth limit: {depth}")
        result = depth_limited_search(start, goal, depth, [start], visited)
        if result is not None:
            return result
        depth += 1

# Main function
def main():
    print("8-Puzzle Problem using Iterative Deepening Search (IDS)\n")
    print("Enter the start state as 9 numbers (0 for blank):")
    # Example input: 1 2 3 4 0 6 7 5 8
    start = tuple(map(int, input().strip().split()))

    print("\nStart State:")
    print_puzzle(start)
    print("Goal State:")
    print_puzzle(goal_state)

    solution_path = iterative_deepening_search(start, goal_state)

    if solution_path:
        print(f"✅ Solution found in {len(solution_path) - 1} moves:\n")
        for step, state in enumerate(solution_path):
            print(f"Step {step}:")
            print_puzzle(state)
    else:
        print("❌ No solution found.")

if __name__ == "__main__":
    main()


'''
8-Puzzle Problem using Iterative Deepening Search (IDS)

Enter the start state as 9 numbers (0 for blank):
1 2 3 0 4 6 7 5 8

Start State:
(1, 2, 3)
(0, 4, 6)
(7, 5, 8)

Goal State:
(1, 2, 3)
(4, 5, 6)
(7, 8, 0)

🔹 Searching at depth limit: 0
Exploring state with Manhattan Distance = 3
(1, 2, 3)
(0, 4, 6)
(7, 5, 8)

🔹 Searching at depth limit: 1
Exploring state with Manhattan Distance = 3
(1, 2, 3)
(0, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(0, 2, 3)
(1, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(1, 2, 3)
(7, 4, 6)
(0, 5, 8)

Exploring state with Manhattan Distance = 2
(1, 2, 3)
(4, 0, 6)
(7, 5, 8)

🔹 Searching at depth limit: 2
Exploring state with Manhattan Distance = 3
(1, 2, 3)
(0, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(0, 2, 3)
(1, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 5
(2, 0, 3)
(1, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(1, 2, 3)
(7, 4, 6)
(0, 5, 8)

Exploring state with Manhattan Distance = 5
(1, 2, 3)
(7, 4, 6)
(5, 0, 8)

Exploring state with Manhattan Distance = 2
(1, 2, 3)
(4, 0, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 3
(1, 0, 3)
(4, 2, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 1
(1, 2, 3)
(4, 5, 6)
(7, 0, 8)

Exploring state with Manhattan Distance = 3
(1, 2, 3)
(4, 6, 0)
(7, 5, 8)

🔹 Searching at depth limit: 3
Exploring state with Manhattan Distance = 3
(1, 2, 3)
(0, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(0, 2, 3)
(1, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 5
(2, 0, 3)
(1, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 6
(2, 4, 3)
(1, 0, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 6
(2, 3, 0)
(1, 4, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(1, 2, 3)
(7, 4, 6)
(0, 5, 8)

Exploring state with Manhattan Distance = 5
(1, 2, 3)
(7, 4, 6)
(5, 0, 8)

Exploring state with Manhattan Distance = 6
(1, 2, 3)
(7, 0, 6)
(5, 4, 8)

Exploring state with Manhattan Distance = 4
(1, 2, 3)
(7, 4, 6)
(5, 8, 0)

Exploring state with Manhattan Distance = 2
(1, 2, 3)
(4, 0, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 3
(1, 0, 3)
(4, 2, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(0, 1, 3)
(4, 2, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 4
(1, 3, 0)
(4, 2, 6)
(7, 5, 8)

Exploring state with Manhattan Distance = 1
(1, 2, 3)
(4, 5, 6)
(7, 0, 8)

Exploring state with Manhattan Distance = 2
(1, 2, 3)
(4, 5, 6)
(0, 7, 8)

Exploring state with Manhattan Distance = 0
(1, 2, 3)
(4, 5, 6)
(7, 8, 0)

✅ Solution found in 3 moves:

Step 0:
(1, 2, 3)
(0, 4, 6)
(7, 5, 8)

Step 1:
(1, 2, 3)
(4, 0, 6)
(7, 5, 8)

Step 2:
(1, 2, 3)
(4, 5, 6)
(7, 0, 8)

Step 3:
(1, 2, 3)
(4, 5, 6)
(7, 8, 0)



...Program finished with exit code 0
Press ENTER to exit console.

'''
