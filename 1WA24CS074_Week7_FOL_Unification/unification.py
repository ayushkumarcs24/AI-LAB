"""
Name : Ayush Kumar
USN  : 1WA24CS074

Unification in First-Order Logic (with failure reasons)

Representation:
  Variable  -> lowercase string starting with a letter, e.g. "x", "y"
  Constant  -> string starting with an uppercase letter, e.g. "Riya", "Apple"
  Compound  -> tuple (symbol, arg1, arg2, ...), e.g. ("Eats", "x", "Apple")
"""


class UnificationError(Exception):
    """Raised when two terms cannot be unified; message holds the reason."""


def is_variable(t):
    return isinstance(t, str) and t[0].islower()


def is_constant(t):
    return isinstance(t, str) and t[0].isupper()


def is_compound(t):
    return isinstance(t, tuple)


def to_str(t):
    if is_compound(t):
        return f"{t[0]}({', '.join(to_str(a) for a in t[1:])})"
    return t


def occurs_check(var, term, theta):
    """True if var occurs inside term (after applying theta)."""
    if var == term:
        return True
    if is_variable(term) and term in theta:
        return occurs_check(var, theta[term], theta)
    if is_compound(term):
        return any(occurs_check(var, arg, theta) for arg in term[1:])
    return False


def unify_var(var, term, theta):
    if var in theta:
        return unify(theta[var], term, theta)
    if is_variable(term) and term in theta:
        return unify(var, theta[term], theta)
    if occurs_check(var, term, theta):
        raise UnificationError(
            f"occurs check: variable '{var}' appears inside {to_str(term)}, "
            f"so it would create an infinite term")
    new_theta = dict(theta)
    new_theta[var] = term
    return new_theta


def unify(t1, t2, theta=None):
    """Return the MGU (dict) of t1 and t2, or raise UnificationError."""
    if theta is None:
        theta = {}
    if t1 == t2:
        return theta
    if is_variable(t1):
        return unify_var(t1, t2, theta)
    if is_variable(t2):
        return unify_var(t2, t1, theta)
    if is_compound(t1) and is_compound(t2):
        if t1[0] != t2[0]:
            raise UnificationError(
                f"symbols differ: '{t1[0]}' and '{t2[0]}' are different, "
                f"cannot unify {to_str(t1)} with {to_str(t2)}")
        if len(t1) != len(t2):
            raise UnificationError(
                f"argument count differs: {to_str(t1)} has {len(t1) - 1}, "
                f"{to_str(t2)} has {len(t2) - 1}")
        for a, b in zip(t1[1:], t2[1:]):
            theta = unify(a, b, theta)
        return theta
    if is_constant(t1) and is_constant(t2):
        raise UnificationError(
            f"different constants: '{t1}' and '{t2}' cannot be made equal")
    raise UnificationError(
        f"cannot unify {to_str(t1)} with {to_str(t2)} "
        f"(a constant cannot match a compound term)")


def substitute(term, theta):
    """Apply substitution theta to term (fully resolving chains)."""
    if is_variable(term):
        return substitute(theta[term], theta) if term in theta else term
    if is_compound(term):
        return (term[0],) + tuple(substitute(a, theta) for a in term[1:])
    return term


def run(e1, e2):
    print(f"Unify({to_str(e1)}, {to_str(e2)})")
    try:
        theta = unify(e1, e2)
    except UnificationError as err:
        print("  Result : FAIL")
        print(f"  Reason : {err}\n")
        return
    mgu = ", ".join(f"{v}/{to_str(substitute(v, theta))}" for v in theta)
    print(f"  MGU    : {{ {mgu} }}")
    print(f"  Unified: {to_str(substitute(e1, theta))}\n")


if __name__ == "__main__":
    print("Name : Ayush Kumar")
    print("USN  : 1WA24CS074")
    print("-" * 50 + "\n")

    # Slide 3 example
    run(("Eats", "x", "Apple"), ("Eats", "Riya", "y"))

    # Slide 2 examples
    run(("P", "x", ("h", "y")), ("P", "Aa", ("f", "z")))        # h vs f
    run(("p", ("f", "A"), ("g", "y")), ("p", "x", "x"))          # f vs g
    run(("Knows", "John", "x"), ("Knows", "x", "Elisabeth"))     # John vs Elisabeth
    run(("Knows", "John", "x"), ("Knows", "y", "Elisabeth"))     # works