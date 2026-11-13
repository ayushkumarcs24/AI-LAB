
# BMSCE - Artificial Intelligence Lab
# Forward Chaining
# Problem: Prove Robert is Criminal

print("======================================")
print("          BMSCE - AI LAB")
print("======================================")
print("Name : AYUSH KUMAR")
print("USN  : 1WA24CS074")
print("Experiment: Forward Chaining")
print("======================================")

# Initial Knowledge Base
facts = [
    ("American", "Robert"),
    ("Missile", "T1"),
    ("Owns", "A", "T1"),
    ("Enemy", "A", "America")
]

# Forward Chaining Function
def forward_chaining(facts):

    new_fact_added = True

    print("\nInitial Facts:")
    for fact in facts:
        print(fact)

    while new_fact_added:
        new_fact_added = False

        # Rule 1: Missile(x) -> Weapon(x)
        for fact in facts.copy():
            if fact[0] == "Missile":
                new = ("Weapon", fact[1])

                if new not in facts:
                    facts.append(new)
                    print("Derived:", new)
                    new_fact_added = True

        # Rule 2: Missile(x) AND Owns(A,x)
        # -> Sells(Robert,x,A)
        for f1 in facts.copy():
            for f2 in facts.copy():

                if (f1[0] == "Missile" and
                    f2[0] == "Owns" and
                    f1[1] == f2[2] and
                    f2[1] == "A"):

                    new = ("Sells", "Robert", f1[1], "A")

                    if new not in facts:
                        facts.append(new)
                        print("Derived:", new)
                        new_fact_added = True

        # Rule 3: Enemy(x,America) -> Hostile(x)
        for fact in facts.copy():
            if (fact[0] == "Enemy" and
                fact[2] == "America"):

                new = ("Hostile", fact[1])

                if new not in facts:
                    facts.append(new)
                    print("Derived:", new)
                    new_fact_added = True

        # Rule 4:
        # American(p) AND Weapon(q) AND
        # Sells(p,q,r) AND Hostile(r)
        # -> Criminal(p)

        for f1 in facts.copy():
            for f2 in facts.copy():
                for f3 in facts.copy():
                    for f4 in facts.copy():

                        if (f1[0] == "American" and
                            f2[0] == "Weapon" and
                            f3[0] == "Sells" and
                            f4[0] == "Hostile"):

                            if (f3[1] == f1[1] and
                                f3[2] == f2[1] and
                                f3[3] == f4[1]):

                                new = ("Criminal", f1[1])

                                if new not in facts:
                                    facts.append(new)
                                    print("Derived:", new)
                                    new_fact_added = True

    return facts


# Execute Forward Chaining
print("\nForward Chaining Process:")
result = forward_chaining(facts)

# Check Goal
print("\n======================================")
print("             FINAL RESULT")
print("======================================")

if ("Criminal", "Robert") in result:
    print("Goal Proved: Robert is Criminal")
else:
    print("Goal Not Proved")

print("======================================")
print("             END OF PROGRAM")
print("======================================")
