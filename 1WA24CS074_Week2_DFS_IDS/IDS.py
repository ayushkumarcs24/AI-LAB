import sys

NAME = "Ayush Kumar"
USN = "1WA24CS074"
HEADER = f"Name: {NAME}\nUSN : {USN}\n" + "=" * 40

# Blank position -> positions it can swap with (tried in this order)
NEIGHBOURS = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7],
}
MOVE_NAME = {-3: "Up", 3: "Down", -1: "Left", 1: "Right"}  # blank's direction


def read_states(text):
    nums = [int(t) for t in text.replace(",", " ").split() if t.isdigit()]
    if len(nums) != 18:
        sys.exit("Need exactly 18 numbers (9 for initial, 9 for goal).")
    init, goal = tuple(nums[:9]), tuple(nums[9:])
    for s in (init, goal):
        if sorted(s) != list(range(9)):
            sys.exit("Each state must contain the digits 0-8 exactly once.")
    return init, goal


def inversions(state):
    t = [x for x in state if x != 0]
    return sum(t[i] > t[j] for i in range(len(t)) for j in range(i + 1, len(t)))


def solvable(init, goal):
    # For a 3x3 board, both states must have the same inversion parity
    return inversions(init) % 2 == inversions(goal) % 2


def neighbours(state):
    """Yield (move_name, new_state) by swapping the blank with each allowed position."""
    z = state.index(0)
    for n in NEIGHBOURS[z]:
        s = list(state)
        s[z], s[n] = s[n], s[z]
        yield MOVE_NAME[n - z], tuple(s)


def depth_limited_dfs(state, goal, limit, path_states, path_moves, on_path, counter):
    """Recursive DFS up to 'limit' moves deep. Cycles are avoided by checking the current path."""
    counter[0] += 1
    if state == goal:
        return True
    if limit == 0:
        return False
    for move, nxt in neighbours(state):
        if nxt in on_path:
            continue
        on_path.add(nxt)
        path_states.append(nxt)
        path_moves.append(move)
        if depth_limited_dfs(nxt, goal, limit - 1, path_states, path_moves, on_path, counter):
            return True
        on_path.remove(nxt)
        path_states.pop()
        path_moves.pop()
    return False


def ids(init, goal, max_depth=31):
    """Run depth-limited DFS with limits 0, 1, 2, ... Returns (moves, states, total_nodes, depth)."""
    total = 0
    for limit in range(max_depth + 1):
        counter = [0]
        path_states, path_moves = [init], []
        found = depth_limited_dfs(init, goal, limit, path_states, path_moves, {init}, counter)
        total += counter[0]
        print(f"  Depth limit {limit:2d}: nodes expanded = {counter[0]}")
        if found:
            return path_moves, path_states, total, limit
    return None, None, total, None


def fmt(state):
    return "\n".join(" ".join("_" if x == 0 else str(x) for x in state[i:i + 3]) for i in (0, 3, 6))


def main():
    print(HEADER)
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else input(
        "Enter initial (9 nums) then goal (9 nums), 0 = blank: ")
    init, goal = read_states(text)

    print("\nInitial state:\n" + fmt(init))
    print("\nGoal state:\n" + fmt(goal))

    if not solvable(init, goal):
        print("\nThis goal is NOT reachable from the initial state (parity mismatch).")
        return

    print("\nRunning IDS...")
    moves, states, total, depth = ids(init, goal)
    if moves is None:
        print("\nNo solution found.")
        return

    print("\nSolution found with IDS")
    print(f"Solution depth (moves)       : {len(moves)}")
    print(f"Total nodes expanded (all iterations): {total}")
    print("\nMoves:", " -> ".join(moves) if moves else "(already at goal)")

    with open("ids_output.txt", "w") as f:
        f.write(HEADER + "\n\n")
        for i, s in enumerate(states):"""
8-Puzzle using Iterative Deepening Search (IDS)

Usage:
    python eight_puzzle_ids.py states.txt
    python eight_puzzle_ids.py            (type the states when prompted)

states.txt: the first 9 numbers are the INITIAL state, the next 9 are the
FINAL (goal) state. Use 0 for the blank. Layout (rows / one line) doesn't matter, e.g.

    1 2 3
    0 4 6
    7 5 8

    1 2 3
    4 5 6
    7 8 0
"""
import sys

NAME = "Ayush Kumar"
USN = "1WA24CS074"
HEADER = f"Name: {NAME}\nUSN : {USN}\n" + "=" * 40

# Blank position -> positions it can swap with (tried in this order)
NEIGHBOURS = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7],
}
MOVE_NAME = {-3: "Up", 3: "Down", -1: "Left", 1: "Right"}  # blank's direction


def read_states(text):
    nums = [int(t) for t in text.replace(",", " ").split() if t.isdigit()]
    if len(nums) != 18:
        sys.exit("Need exactly 18 numbers (9 for initial, 9 for goal).")
    init, goal = tuple(nums[:9]), tuple(nums[9:])
    for s in (init, goal):
        if sorted(s) != list(range(9)):
            sys.exit("Each state must contain the digits 0-8 exactly once.")
    return init, goal


def inversions(state):
    t = [x for x in state if x != 0]
    return sum(t[i] > t[j] for i in range(len(t)) for j in range(i + 1, len(t)))


def solvable(init, goal):
    # For a 3x3 board, both states must have the same inversion parity
    return inversions(init) % 2 == inversions(goal) % 2


def neighbours(state):
    """Yield (move_name, new_state) by swapping the blank with each allowed position."""
    z = state.index(0)
    for n in NEIGHBOURS[z]:
        s = list(state)
        s[z], s[n] = s[n], s[z]
        yield MOVE_NAME[n - z], tuple(s)


def depth_limited_dfs(state, goal, limit, path_states, path_moves, on_path, counter):
    """Recursive DFS up to 'limit' moves deep. Cycles are avoided by checking the current path."""
    counter[0] += 1
    if state == goal:
        return True
    if limit == 0:
        return False
    for move, nxt in neighbours(state):
        if nxt in on_path:
            continue
        on_path.add(nxt)
        path_states.append(nxt)
        path_moves.append(move)
        if depth_limited_dfs(nxt, goal, limit - 1, path_states, path_moves, on_path, counter):
            return True
        on_path.remove(nxt)
        path_states.pop()
        path_moves.pop()
    return False


def ids(init, goal, max_depth=31):
    """Run depth-limited DFS with limits 0, 1, 2, ... Returns (moves, states, total_nodes, depth)."""
    total = 0
    for limit in range(max_depth + 1):
        counter = [0]
        path_states, path_moves = [init], []
        found = depth_limited_dfs(init, goal, limit, path_states, path_moves, {init}, counter)
        total += counter[0]
        print(f"  Depth limit {limit:2d}: nodes expanded = {counter[0]}")
        if found:
            return path_moves, path_states, total, limit
    return None, None, total, None


def fmt(state):
    return "\n".join(" ".join("_" if x == 0 else str(x) for x in state[i:i + 3]) for i in (0, 3, 6))


def main():
    print(HEADER)
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else input(
        "Enter initial (9 nums) then goal (9 nums), 0 = blank: ")
    init, goal = read_states(text)

    print("\nInitial state:\n" + fmt(init))
    print("\nGoal state:\n" + fmt(goal))

    if not solvable(init, goal):
        print("\nThis goal is NOT reachable from the initial state (parity mismatch).")
        return

    print("\nRunning IDS...")
    moves, states, total, depth = ids(init, goal)
    if moves is None:
        print("\nNo solution found.")
        return

    print("\nSolution found with IDS")
    print(f"Solution depth (moves)       : {len(moves)}")
    print(f"Total nodes expanded (all iterations): {total}")
    print("\nMoves:", " -> ".join(moves) if moves else "(already at goal)")

    with open("ids_output.txt", "w") as f:
        f.write(HEADER + "\n\n")
        for i, s in enumerate(states):
            f.write(f"Step {i}" + (f"  (move: {moves[i - 1]})" if i else "  (initial)") + "\n")
            f.write(fmt(s) + "\n\n")
    print("\nFull step-by-step path saved to ids_output.txt")


if __name__ == "__main__":
    main()