# Exercise 04: the computer grows up

|  |  |
|---|---|
| **AI level** | **0**: no AI, and inline completion stays off |
| **Part 1** | in class, Fri Oct 23 |
| **Part 2** | at home (the week of Oct 26 has no classes) |
| **Due** | Thu Nov 5, 17:00, as a pull request |
| **Review due** | Tue Nov 10, 17:00 (author answers before the Wednesday session on Nov 11) |

## Getting started

```
git checkout main
git pull
git checkout -b ex04-<login>
```

Copy the folder `exercises/ex04` to `students/<login>/ex04` and work only in the copy.
Check your work with `uv run pytest students/<login>/ex04` and see your answers with
`uv run python students/<login>/ex04/ex04.py`.

This exercise extends the computer from Exercise 2. You may copy your own Ex 2 `step` and
`run` into `ex04.py` as a starting point; their parameters change a little (see below).

## The program file

Programs now come as a text file, `diagnostic.txt`. Open it: it's the same kind of list of
numbers as before, but written for people to read.

- Numbers are separated by commas and/or line breaks.
- A `#` starts a **comment**, which runs to the end of its line. Comments are for humans;
  the computer never sees them.
- Spaces and blank lines don't matter.

```
# adds two numbers
1, 5, 6, 0    # 0: add
99            # 4: halt
20, 22
```

is the program `[1, 5, 6, 0, 99, 20, 22]`.

`ex04.py` gives you `PROGRAM_FILE`, the path to `diagnostic.txt` *next to `ex04.py`*. Use it
rather than just `"diagnostic.txt"`: a bare file name is looked up in the folder you run
Python **from**, which for `uv run` is the top of the repository.

## Parameter modes

So far, every parameter was an **address**: `1, 5, 6, 0` adds the values *at* positions 5
and 6. That's **position mode** (mode 0). New is **immediate mode** (mode 1): the parameter
*is* the value. In immediate mode, `5` means the number 5.

The mode of each parameter is stored in the opcode itself. The last two digits are the
opcode; the digits before them are the modes of the parameters, read **right to left**: the
hundreds digit is the mode of the first parameter, the thousands digit of the second, the
ten-thousands digit of the third. Missing digits are 0.

**Example:** `1002, 4, 3, 4, 33`

| Digits of 1002 | Meaning |
|---|---|
| `02` | opcode 2, multiply |
| `0` (hundreds) | first parameter, `4`, in position mode: the value at position 4, which is 33 |
| `1` (thousands) | second parameter, `3`, in immediate mode: the number 3 |
| (missing, so `0`) | third parameter, `4`, in position mode: write to position 4 |

33 × 3 = 99 is written to position 4. The next instruction is at position 4, and it's 99:
halt.

A parameter the instruction **writes to** is always in position mode. Numbers can be negative
now: `1101, 100, -1, 4, 0` writes 99 to position 4.

## Input and output

Two new instructions, each with **one** parameter, so they're 2 positions long:

- **3: input.** Take the next number from the program's inputs and write it to the address
  given by the parameter. `3, 50` stores an input at position 50.
- **4: output.** Output the value of the parameter. `4, 50` outputs the value at position 50;
  `104, 50` outputs the number 50.

`step(memory, position, inputs, outputs)` gets two lists: opcode 3 takes the first number out
of `inputs`, opcode 4 appends to `outputs`. `run(memory, inputs)` returns all outputs as a
list. `[3, 0, 4, 0, 99]` outputs whatever it was given as input.

## Part 1 (in class)

1. `parse_program(text)`: turn the text of a program file into a list of ints.
2. `load_program(path)`: read the file at `path` and return its program. Use your
   `parse_program`.
3. `decode(instruction)`: `decode(1002) == (2, [0, 1, 0])`.
4. `parameter(memory, position, n)`: the value of the n-th parameter of the instruction at
   `position`, in whatever mode it has.
5. `step` and `run`: opcodes 1, 2, 3, 4 and 99, with parameter modes. An unknown opcode now
   **raises a `ValueError`**, with a message that says which opcode at which position.
   `run` must not change the `inputs` list it was given.

`diagnostic.txt` is a program that checks your computer. It first reads a **system ID**. With
ID 1 it runs a series of checks; each one outputs **0** if your computer did the right thing.
The last output is a **diagnostic code**. If any other output isn't 0, the comments in
`diagnostic.txt` tell you which check produced it. Answer 2 is the output for ID 1.

## Part 2 (at home)

Part 2 builds on **your own** Part 1 code.

Run `diagnostic.txt` with ID 5. Your Part 1 computer should stop with a `ValueError` about an
unknown opcode, which is what this part adds. Four new instructions; parameter modes work as
before:

- **5: jump-if-true**, 2 parameters. If the first is not zero, the next instruction is at
  the position given by the second. Otherwise, carry on with the next instruction as usual.
- **6: jump-if-false**, 2 parameters. The same, but jump if the first is zero.
- **7: less than**, 3 parameters. If the first is less than the second, write 1 to the
  address given by the third, otherwise 0.
- **8: equals**, 3 parameters. If the first equals the second, write 1 to the address given by
  the third, otherwise 0.

A jump means the next instruction is no longer always "the next one along": `step` returns
wherever execution continues.

1. Add opcodes 5 to 8 to `step`.
2. `MAX_OF_TWO` reads two numbers and outputs the larger one. Answer 3 runs it.
3. Answer 4 is the output of `diagnostic.txt` for ID 5. If a jump goes wrong, a program can
   loop forever: stop it with Ctrl+C.
4. What does your computer do when a program reads input but `inputs` is empty? Decide what
   it *should* do, write that into `step`'s description (the text in triple quotes), and add a
   test for it.
5. **Add at least two more tests of your own** at the end of `test_ex04.py`. Write each test
   case down first: which input, which expected result, and which case it covers.

## Your pull request

- Title: `ex04 <login>`
- Paste the output of `uv run python students/<login>/ex04/ex04.py` under **Result**.
- CI must be green: all tests pass, ruff is happy.
