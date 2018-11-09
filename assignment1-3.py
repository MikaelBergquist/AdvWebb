tree = []
with open("tree.txt", "r") as f:
    for line in f:
        tree.append(line.rstrip())

print(list_solver(tree))