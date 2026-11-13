
import re

print("======================================")
print("           BMSCE - AI LAB")
print("======================================")
print("Name : AYUSH KUMAR")
print("USN  : YOUR_USN")
print("Experiment: Forward Chaining")
print("======================================")

print("\nEnter the problem statement")
print("(Press Enter twice to finish):")

lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

statement = " ".join(lines)

# Extract information from statement
seller_match = re.search(
    r"sold to it by ([A-Za-z]+)", statement, re.I
)
country_match = re.search(
    r"Country ([A-Za-z]+)", statement, re.I
)

seller = seller_match.group(1).capitalize() if seller_match else "Robert"
country = country_match.group(1).upper() if country_match else "A"

# Generate FOL facts
facts = []

if re.search(r"American citizen|American", statement, re.I):
    facts.append(("American", seller))

if re.search(r"missile", statement, re.I):
    facts.append(("Missile", "T1"))

if re.search(r"enemy of America", statement, re.I):
    facts.append(("Enemy", country, "America"))

if re.search(r"has some missiles|owns.*missiles", statement, re.I):
    facts.append(("Owns", country, "T1"))

# Generate FOL rules
rules = [
    "Missile(x) -> Weapon(x)",
    "Enemy(x, America) -> Hostile(x)",
    "Missile(x) AND Owns(A, x) -> Sells(Robert, x, A)",
    "American(p) AND Weapon(q) AND Sells(p,q,r) AND Hostile(r) -> Criminal(p)"
]

# Replace names in rules
rules[2] = rules[2].replace("Robert", seller).replace("A", country)
rules[3] = rules[3].replace("Robert", seller)

print("\n========== GENERATED FOL ==========")

print("\nFacts:")
for fact in facts:
    print(fact)

print("\nRules:")
for rule in rules:
    print(rule)

# Forward Chaining
changed = True

while changed:
    changed = False

    for fact in facts.copy():

        # Missile(x) -> Weapon(x)
        if fact[0] == "Missile":
            new = ("Weapon", fact[1])

            if new not in facts:
                facts.append(new)
                print("Derived:", new)
                changed = True

        # Enemy(x, America) -> Hostile(x)
        if fact[0] == "Enemy":
            new = ("Hostile", fact[1])

            if new not in facts:
                facts.append(new)
                print("Derived:", new)
                changed = True

    # Missile(x) AND Owns(A,x) -> Sells(Robert,x,A)
    for f1 in facts.copy():
        for f2 in facts.copy():

            if (f1[0] == "Missile" and
                f2[0] == "Owns" and
                f2[1] == country and
                f1[1] == f2[2]):

                new = ("Sells", seller, f1[1], country)

                if new not in facts:
                    facts.append(new)
                    print("Derived:", new)
                    changed = True

    # Final criminal rule
    if (("American", seller) in facts):

        for f1 in facts.copy():
            for f2 in facts.copy():
                for f3 in facts.copy():

                    if (f1[0] == "Weapon" and
                        f2[0] == "Sells" and
                        f3[0] == "Hostile"):

                        if (f2[1] == seller and
                            f2[2] == f1[1] and
                            f2[3] == f3[1]):

                            new = ("Criminal", seller)

                            if new not in facts:
                                facts.append(new)
                                print("Derived:", new)
                                changed = True

print("\n========== FINAL RESULT ==========")

if ("Criminal", seller) in facts:
    print("FOL Query: Criminal(" + seller + ")")
    print("Goal Proved:", seller, "is Criminal")
else:
    print("Goal cannot be proved from the given statement.")

print("======================================")
