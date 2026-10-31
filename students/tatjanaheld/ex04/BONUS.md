# Exercise 04, bonus: relative mode

Two weeks is a long time for this exercise, so here is more for anyone who wants it. It's
**optional**: your PR counts without it. Exercise 6 runs a game on the computer and needs
these features. If you do the bonus, you can run the game on **your own** computer; if not,
you'll get a complete one to use.

AI level 0, like the rest of this exercise.

1. **Memory beyond the program.** Programs may now read and write any address `>= 0`, also
   far beyond the end of the list they came in. Every address not in the program holds 0
   until something is written there. `4, 1000, 99` outputs 0. A negative address is an
   error.
2. **Relative mode (mode 2).** The computer keeps one more number, the **relative base**,
   which starts at 0. A parameter in relative mode is an address counted from the relative
   base: with base 50, a relative parameter `7` means address 57, and `-7` means address 43.
   Relative mode works for parameters that are read *and* for parameters that are written to.
3. **Opcode 9: adjust the relative base**, 1 parameter. Add the parameter's value to the
   relative base. `109, 5` adds 5; `109, -3` subtracts 3.
4. `run_bonus(memory, inputs)` in your `ex04.py`: like `run`, with all of the above. Keep
   `step` and `run` as they are, so the Part 1 and 2 tests still pass.

The relative base has to survive from one instruction to the next, and `step` needs it.
Where do you keep it? There's more than one reasonable answer: pick one and say why in your
PR. (Exercise 6 has a neat answer to this.)

Copy `test_ex04_bonus.py` into your `students/<login>/ex04` folder (if you copied the folder
before it existed); its tests are skipped until `ex04.py` has a `run_bonus`. The last one runs
`FACTORIAL`, a program that reads `n` and outputs `n!`, **recursively**: every call keeps its
argument and result in its own little area of memory, found through the relative base, and
opcode 9 moves the base from one call's area to the next and back. That's what relative mode
is for.

If you do the bonus, say so in your PR description, so your reviewer knows to look at it.
