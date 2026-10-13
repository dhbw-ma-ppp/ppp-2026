def step(memory, position):
    """Execute the instruction that starts at `position` in memory.

    Opcode 1 adds, opcode 2 multiplies, opcode 99 halts (see README.md).
    Return the position of the next instruction, or None if the opcode is 99.
    """
    if memory[position] == 1:
        memory[memory[position + 3]] = memory[memory[position + 1]] + memory[memory[position + 2]]
        print(memory)
    elif memory[position] == 2:
        memory[memory[position + 3]] = memory[memory[position + 1]] * memory[memory[position + 2]]
        print(memory)
    elif memory[position] == 99:
        return None
    else:
        return -1
    return position + 4


memory = [1, 0, 0, 0, 99]
print(step(memory, 0))
