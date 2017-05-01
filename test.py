from __future__ import print_function
with open("scores.txt") as f:
   file = eval(f.read())

print(*file, sep="\n")