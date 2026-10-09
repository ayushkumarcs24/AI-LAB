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


def dfs(init, goal):
    """Iterative DFS with a visited set. Returns (path_of_moves, states, nodes_expanded)."""
    stack = [(init, None)]           # (state, parent_state)
    parent = {}                      # state -> (parent_state, move)
    visited = set()
    expanded = 0
    pending_move = {init: None}

    while stack:
        state, par = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        parent[state] = (par, pending_move.get(state))
        expanded += 1

        if state == goal:
            moves, states = [], [state]
            cur = state
            while parent[cur][0] is not None:
                p, m = parent[cur]
                moves.append(m)
                states.append(p)
                cur = p
            return moves[::-1], states[::-1], expanded

        # push in reverse so that the first allowed position is explored first
        for name, nxt in reversed(list(neighbours(state))):
            if nxt not in visited:
                pending_move[nxt] = name
                stack.append((nxt, state))
    return None, None, expanded


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

    moves, states, expanded = dfs(init, goal)
    if moves is None:
        print("\nNo solution found.")
        return

    print("\nSolution found with DFS")
    print(f"Path length (moves): {len(moves)}")
    print(f"Nodes expanded     : {expanded}")

    with open("dfs_output.txt", "w") as f:
        f.write(HEADER + "\n\n")
        for i, s in enumerate(states):
            f.write(f"Step {i}" + (f"  (move: {moves[i - 1]})" if i else "  (initial)") + "\n")
            f.write(fmt(s) + "\n\n")
    print("Full step-by-step path saved to dfs_output.txt")

    if len(moves) <= 30:
        print("\nMoves:", " -> ".join(moves))
    else:
        print("\n(Path is long - DFS does not find shortest paths. First 10 moves:)",
              " -> ".join(moves[:10]), "...")


if __name__ == "__main__":
    main()