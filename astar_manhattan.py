'''
IMplementation of A* and Manhatan distance algorithm in Python
'''


import heapq

class PuzzleState:
    def __init__(self, board, goal, g=0, h=0, parent=None):
        self.board = board
        self.goal = goal
        self.g = g  # cost so far (depth)
        self.h = h  # heuristic value
        self.f = g + h  # total cost
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f

    def get_blank_pos(self):
        return self.board.index(0)

    def get_moves(self):
        """Return possible moves for blank tile"""
        moves = []
        blank = self.get_blank_pos()
        x, y = divmod(blank, 3)

        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_blank = nx * 3 + ny
                new_board = self.board[:]
                new_board[blank], new_board[new_blank] = new_board[new_blank], new_board[blank]
                moves.append(new_board)
        return moves

    def is_goal(self):
        return self.board == self.goal

    def print_path(self):
        path = []
        state = self
        while state:
            path.append(state.board)
            state = state.parent
        path.reverse()
        print("\nSolution Path:")
        for p in path:
            print_board(p)

def print_board(board):
    for i in range(0, 9, 3):
        print(board[i:i+3])
    print()

# ---------- Heuristics ----------
def misplaced_tiles(board, goal):
    return sum(1 for i in range(9) if board[i] != 0 and board[i] != goal[i])

def manhattan_distance(board, goal):
    distance = 0
    for i in range(9):
        if board[i] != 0:
            goal_index = goal.index(board[i])
            x1, y1 = divmod(i, 3)
            x2, y2 = divmod(goal_index, 3)
            distance += abs(x1 - x2) + abs(y1 - y2)
    return distance

# ---------- A* Search ----------
def a_star(start, goal, heuristic):
    open_list = []
    closed_set = set()
    start_state = PuzzleState(start, goal, g=0, h=heuristic(start, goal))
    heapq.heappush(open_list, start_state)

    while open_list:
        current = heapq.heappop(open_list)

        if current.is_goal():
            current.print_path()
            return True

        closed_set.add(tuple(current.board))

        for move in current.get_moves():
            if tuple(move) in closed_set:
                continue
            g = current.g + 1
            h = heuristic(move, goal)
            neighbor = PuzzleState(move, goal, g, h, current)
            heapq.heappush(open_list, neighbor)

    return False

# ---------- Main Execution ----------
if __name__ == "__main__":
    # Example Initial and Goal states
    initial_state = [2, 8, 3,
                     1, 6, 4,
                     0, 7, 5]

    goal_state = [1, 2, 3,
                  8, 0, 4,
                  7, 6, 5]

    print("Case 1: A* with Misplaced Tiles Heuristic")
    a_star(initial_state, goal_state, misplaced_tiles)

    print("Case 2: A* with Manhattan Distance Heuristic")
    a_star(initial_state, goal_state, manhattan_distance)







'''
Case 1: A* with Misplaced Tiles Heuristic

Solution Path:
[2, 8, 3]
[1, 6, 4]
[0, 7, 5]

[2, 8, 3]
[1, 6, 4]
[7, 0, 5]

[2, 8, 3]
[1, 0, 4]
[7, 6, 5]

[2, 0, 3]
[1, 8, 4]
[7, 6, 5]

[0, 2, 3]
[1, 8, 4]
[7, 6, 5]

[1, 2, 3]
[0, 8, 4]
[7, 6, 5]

[1, 2, 3]
[8, 0, 4]
[7, 6, 5]

Case 2: A* with Manhattan Distance Heuristic

Solution Path:
[2, 8, 3]
[1, 6, 4]
[0, 7, 5]

[2, 8, 3]
[1, 6, 4]
[7, 0, 5]

[2, 8, 3]
[1, 0, 4]
[7, 6, 5]

[2, 0, 3]
[1, 8, 4]
[7, 6, 5]

[0, 2, 3]
[1, 8, 4]
[7, 6, 5]

[1, 2, 3]
[0, 8, 4]
[7, 6, 5]

[1, 2, 3]
[8, 0, 4]
[7, 6, 5]


=== Code Execution Successful ===
'''
