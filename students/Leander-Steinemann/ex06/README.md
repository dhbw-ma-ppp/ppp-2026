# Exercise 06: Breakout

|  |  |
|---|---|
| **AI level** | **1**: AI may **explain**, it may not write code for you (as in exercise 5). Inline completion stays off. |
| **Part 1** | in class, Fri Nov 13, **no AI**. Anything you finish at home falls under level 1. |
| **Part 2** | at home, AI level 1 |
| **Due** | Thu Nov 19, 17:00, as a pull request |
| **Review due** | Tue Nov 24, 17:00 (author answers before the Wednesday session on Nov 25) |

## Getting started

```
git checkout main
git pull
git checkout -b ex06-<login>
```

Copy the folder `exercises/ex06` to `students/<login>/ex06` and work only in the copy. Check
your work with `uv run pytest students/<login>/ex06` and see your answers with
`uv run python students/<login>/ex06/ex06.py`.

## AI level 1: explanations, not code

Same rules as exercise 5: you may ask an AI to explain a concept, an error message, or how
a library function works in general. You may not ask it for code for this exercise,
paste your code in for it to fix, or paste the task in. Under **AI use** in your PR: the
questions you asked, and in two or three sentences, in your own words, what you took from
the answers. If you didn't use AI, write "none".

## The game

`breakout.txt` is an IntCode program: a Breakout game. A ball flies around a walled screen
and destroys blocks, and you move a paddle at the bottom to keep the ball in play.

`intcode.py` is a complete IntCode computer, written as functions like yours from exercise 4,
with the bonus included: relative mode, opcode 9, and memory beyond the end of the program.
You don't need to change it. **If you did the exercise 4 bonus**, you may use your own
functions instead: copy them into `intcode.py`, keeping the names and what they return.

The program **outputs** three numbers per tile: `x`, `y` and the tile. `x` counts from the
left, `y` from the top, both from 0. The tiles are

| Tile | Meaning |
|---|---|
| 0 | empty |
| 1 | wall (the ball bounces off it) |
| 2 | block (the ball bounces off it and destroys it) |
| 3 | paddle (the ball bounces off it) |
| 4 | ball |

Three numbers `-1, 0, s` aren't a tile: they set the **score** display to `s`.

At the start, the program draws the whole screen, then waits for an **input**: the joystick.
`-1` moves the paddle left, `1` right, `0` leaves it where it is. After every input, the ball
moves on and the program outputs only what changed (for example the ball's old position as
empty, its new one as ball). That's one **frame**. The game ends, and the program halts, when
the last block is gone or when the ball falls past the paddle.

Your exercise 4 `run` got all its inputs at the start. That doesn't work here: which input
to give depends on what the program has output so far. So the computer must be able to stop
when it needs an input, and carry on later from exactly where it stopped, with its memory,
position and relative base intact. That state belongs together, in an object.

## Part 1 (in class, no AI)

1. `class Computer`:
   - `Computer(program)` makes a computer that will run `program` from position 0. It works
     on its **own copy** of the program: running it must not change `program`, and two
     computers made from the same program don't affect each other.
   - It has an attribute `halted`, `False` until the program has reached opcode 99.
   - `computer.run(inputs)` adds `inputs` to the inputs the computer hasn't used yet, then
     executes instructions until the program halts **or** reaches an input instruction
     (opcode 3) with no input left. It returns the list of numbers output **during this
     call**. The next call carries on from there.
   - Use `step` and `decode` from `intcode.py`. Look at `step`'s docstring: which state does
     it need, and what does it give back?
2. `count_tiles(outputs, tile)`: how many triples in `outputs` show this tile. Score triples
   don't count.

Answer 1: how many blocks are on the screen when the game starts? Run the game until it
first asks for input, and count.

## Part 2 (at home, AI level 1)

1. **A dataclass `Game`** for what's on the screen. Fields, all with defaults, so `Game()`
   works:
   - `tiles`: a dict from `(x, y)` to the tile there, empty at the start;
   - `score`: the score, 0 at the start;
   - `scores`: a list of the score after each `update`, empty at the start;
   - `ball` and `paddle`: the `(x, y)` where the ball and the paddle were last drawn, `None`
     until then (there is only ever one ball and one paddle).

   Methods:
   - `update(outputs)`: apply the outputs of one `run` call to the screen, the score and
     `ball` and `paddle`, then append the score to `scores`;
   - `count(tile)`: how many positions show that tile.

   Give every field and method type annotations.
2. `screen_rows(game)`: the screen as a list of rows, so that `screen_rows(game)[y][x]` is the
   tile at `(x, y)`. The screen is as wide and as tall as the positions in `tiles` need.

   `draw(game)`: the screen as text, one line per row and one character per tile, as given in
   `SYMBOLS` (`#` wall, `=` block, `-` paddle, `o` ball, a space for empty). The lines are
   joined with `"\n"`, without one at the end. `ex06.py` prints the screen at the start and at
   the end of the game.
3. **Controllers.** A controller decides the joystick input from the game: a class with a
   method `choose(self, game)` that returns -1, 0 or 1. `Controller` and `Stay` are given.
   Fill in `Autopilot`'s `choose`, so that it plays the game for you: it keeps the ball in
   play until every block is gone. How it decides is up to you.
4. `play(program, controller)`: make a `Computer` and a `Game`, run the program until it
   first needs input, then give it one input per frame, chosen by `controller`, until it
   halts. Return the `Game`.

   Answer 2: the score at the end with `Stay`. Answer 3: the score at the end with
   `Autopilot`, and how many frames it took. If your game never ends, find out why: is the
   ball stuck, or is your controller?
5. **Add at least two more tests of your own** at the end of `test_ex06.py`. Write each test
   case down first: which input, which expected result, and which case it covers.

## Optional

None of these count towards anything; they're for fun, and we haven't covered the tools in
class. Puzzling that out is part of it.

- **Play it yourself.** A controller `Keyboard` that prints `draw(game)` and the score, and
  reads `a`, `d` or nothing with `input()`.
- **A faster controller:** one that clears all blocks in fewer frames than your `Autopilot`.
- **A picture, or a movie of the whole game.** The usual library for pictures is
  matplotlib (`imshow` draws a grid of numbers as coloured squares). It isn't part of our
  setup yet; we'll add it when we get to data analysis. Until then, put that code in a separate
  file, `students/<login>/ex06/bonus.py`, and run it with
  `uv run --with matplotlib python students/<login>/ex06/bonus.py`. Don't import matplotlib in
  `ex06.py` (the tests would fail without it), and don't change `pyproject.toml`. Commit the
  picture or movie if it's small (a GIF of a few hundred KB is fine), and say in the PR how you
  made it.

## Your pull request

- Title: `ex06 <login>`
- Paste the output of `uv run python students/<login>/ex06/ex06.py` under **Result** (in a
  code block, so the screens keep their shape).
- Under **AI use**: your questions and what you took from the answers (see above).
- CI must be green: all tests pass, ruff is happy.
