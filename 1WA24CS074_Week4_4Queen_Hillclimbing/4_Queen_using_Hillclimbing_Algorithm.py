N = 4

def heuristic(state):
    """Number of attacking pairs (state[i] = column of queen in row i)."""
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                h += 1
    return h

def best_neighbour(state):
    """Swap columns of two queens; first best swap wins ties."""
    best, best_h, best_swap = None, float("inf"), None
    for i in range(N):
        for j in range(i + 1, N):
            nb = state[:]
            nb[i], nb[j] = nb[j], nb[i]
            hv = heuristic(nb)
            if hv < best_h:
                best, best_h, best_swap = nb, hv, (i + 1, j + 1)
    return best, best_h, best_swap

def print_board(state):
    print("     " + " ".join(f"c{c+1}" for c in range(N)))
    for r in range(N):
        row = " ".join(" Q" if state[r] == c + 1 else " ." for c in range(N))
        print(f" r{r+1} {row}")

def hill_climbing(state):
    moves = 0
    while True:
        h = heuristic(state)
        print(f"\nState: {state}   h = {h}")
        print_board(state)
        if h == 0:
            print("\nGoal reached.")
            return state, moves
        nb, nb_h, swap = best_neighbour(state)
        if nb_h >= h:
            print("\nStuck at a local minimum. No better neighbour.")
            return state, moves
        print(f"Best neighbour: swap rows {swap} -> {nb}, h = {nb_h}")
        state = nb
        moves += 1

if __name__ == "__main__":
    print("=" * 40)
    print("Name : Ayush Kumar")
    print("USN  : 1WA24CS074")
    print("=" * 40)
    print("4-Queens using Hill Climbing\n")

    while True:
        try:
            cols = list(map(int, input(
                "Enter column (1-4) of the queen in rows 1 to 4, space separated: ").split()))
            if len(cols) == N and sorted(cols) == list(range(1, N + 1)):
                break
            print("Enter 4 different numbers from 1 to 4 (one queen per column).")
        except ValueError:
            print("Enter integers only.")

    final, moves = hill_climbing(cols)

    print("\n" + "=" * 40)
    print("Final state     :", final)
    print("Final h         :", heuristic(final))
    print("Path cost (moves):", moves)
    print("=" * 40)
    print("Name : Ayush Kumar | USN : 1WA24CS074")