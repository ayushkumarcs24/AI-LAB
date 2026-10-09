
import sys
import heapq

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


def h_misplaced(state, goal):
    """h(n): number of tiles (excluding the blank) not in their goal position."""
    return sum(1 for a, b in zip(state, goal) if a != 0 and a != b)


def astar(init, goal, heuristic=h_misplaced):
    """A* search. Returns (moves, states, nodes_expanded, nodes_generated, f_values)."""
    counter = 0                                   # tie-breaker: FIFO among equal f
    h0 = heuristic(init, goal)
    open_list = [(h0, counter, init)]             # (f, order, state)
    g_cost = {init: 0}
    parent = {init: (None, None)}                 # state -> (parent_state, move)
    closed = set()
    expanded, generated = 0, 1

    while open_list:
        f, _, state = heapq.heappop(open_list)
        if state in closed:
            continue
        closed.add(state)
        expanded += 1

        if state == goal:
            moves, states = [], [state]
            cur = state
            while parent[cur][0] is not None:
                p, m = parent[cur]
                moves.append(m)
                states.append(p)
                cur = p
            moves, states = moves[::-1], states[::-1]
            info = [(g_cost[s], heuristic(s, goal)) for s in states]
            return moves, states, expanded, generated, info

        g = g_cost[state] + 1
        for move, nxt in neighbours(state):
            if nxt in closed:
                continue
            if nxt not in g_cost or g < g_cost[nxt]:
                g_cost[nxt] = g
                parent[nxt] = (state, move)
                counter += 1
                generated += 1
                heapq.heappush(open_list, (g + heuristic(nxt, goal), counter, nxt))
    return None, None, expanded, generated, None


def fmt(state):
    return "\n".join(" ".join("_" if x == 0 else str(x) for x in state[i:i + 3]) for i in (0, 3, 6))


def main():
    print(HEADER)
    text = open(sys.argv[1]).read() if len(sys.argv) > 1 else input(
        "Enter initial (9 nums) then goal (9 nums), 0 = blank: ")
    init, goal = read_states(text)

    print("\nInitial state:\n" + fmt(init))
    print("\nGoal state:\n" + fmt(goal))
    print("\nCase 1: f(n) = g(n) + h(n), g = depth, h = number of misplaced tiles")

    if not solvable(init, goal):
        print("\nThis goal is NOT reachable from the initial state (parity mismatch).")
        return

    moves, states, expanded, generated, info = astar(init, goal)
    if moves is None:
        print("\nNo solution found.")
        return

    print("\nSolution found with A*")
    print(f"Solution depth (moves) : {len(moves)}")
    print(f"Nodes expanded         : {expanded}")
    print(f"Nodes generated        : {generated}")
    print("\nMoves:", " -> ".join(moves) if moves else "(already at goal)")

    with open("astar_case1_output.txt", "w") as f:
        f.write(HEADER + "\n")
        f.write("A* Case 1: g(n) = depth, h(n) = misplaced tiles\n\n")
        for i, s in enumerate(states):
            g, h = info[i]
            f.write(f"Step {i}" + (f"  (move: {moves[i - 1]})" if i else "  (initial)")
                    + f"   g = {g}, h = {h}, f = {g + h}\n")
            f.write(fmt(s) + "\n\n")
    print("\nFull step-by-step path (with g, h, f) saved to astar_case1_output.txt")


if __name__ == "__main__":
    main()