import random

N = 8

def heuristic(state):
    """Number of attacking pairs (state[i] = column of queen in row i)."""
    h = 0
    for i in range(N):
        for j in range(i + 1, N):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                h += 1
    return h

def best_neighbour(state):
    """Swap columns of two queens (28 neighbours); first best swap wins ties."""
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

def hill_climbing(state, verbose=True):
    moves = 0
    while True:
        h = heuristic(state)
        if verbose:
            print(f"\nState: {state}   h = {h}")
            print_board(state)
        if h == 0:
            return state, moves, True
        nb, nb_h, swap = best_neighbour(state)
        if nb_h >= h:
            if verbose:
                print("\nStuck at a local minimum. No better neighbour.")
            return state, moves, False
        if verbose:
            print(f"Best neighbour: swap rows {swap} -> {nb}, h = {nb_h}")
        state = nb
        moves += 1

if __name__ == "__main__":
    print("=" * 50)
    print("Name : Ayush Kumar")
    print("USN  : 1WA24CS074")
    print("=" * 50)
    print("8-Queens using Hill Climbing\n")

    while True:
        try:
            cols = list(map(int, input(
                "Enter column (1-8) of the queen in rows 1 to 8, space separated: ").split()))
            if len(cols) == N and sorted(cols) == list(range(1, N + 1)):
                break
            print("Enter 8 different numbers from 1 to 8 (one queen per column).")
        except ValueError:
            print("Enter integers only.")

    print("\n--- Run from your input ---")
    final, moves, solved = hill_climbing(cols)

    # Hill climbing can get stuck for 8 queens, so restart from random states
    restarts = 0
    while not solved and restarts < 1000:
        restarts += 1
        start = random.sample(range(1, N + 1), N)
        final, moves, solved = hill_climbing(start, verbose=False)

    if restarts:
        print(f"\nYour input got stuck. Solved after {restarts} random restart(s).")
        print("Final board:")
        print_board(final)

    print("\n" + "=" * 50)
    print("Final state      :", final)
    print("Final h          :", heuristic(final))
    print("Path cost (moves):", moves, "(moves in the successful run)")
    print("=" * 50)
    print("Name : Ayush Kumar | USN : 1WA24CS074")