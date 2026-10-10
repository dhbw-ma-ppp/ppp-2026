from puzzle_input import INSTRUCTIONS

pos = 0
counter = 0

for char in INSTRUCTIONS:
    counter += 1

    if char == "(":
        pos += 1
    else:
        pos -= 1

    if pos == -1:
        print(counter)
        break
