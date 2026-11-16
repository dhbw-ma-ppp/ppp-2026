import ex06
from ex06 import (
    BALL,
    BLOCK,
    PADDLE,
    WALL,
    PROGRAM_FILE,
    RUNNING_TOTAL,
    TINY_GAME,
    Autopilot,
    Computer,
    Controller,
    Stay,
    count_tiles,
    load_program,
)

# Part 2's `Game` doesn't exist until you write it, so its tests use `ex06.Game`: they fail
# one by one instead of all at once.

# ---------------------------------------------------------------- Part 1


def test_run_until_halt():
    computer = Computer([104, 7, 104, 8, 99])
    assert computer.run([]) == [7, 8]
    assert computer.halted


def test_not_halted_at_the_start():
    assert not Computer([99]).halted


def test_pauses_without_input():
    computer = Computer(RUNNING_TOTAL)
    assert computer.run([]) == []
    assert not computer.halted


def test_carries_on_after_a_pause():
    computer = Computer(RUNNING_TOTAL)
    assert computer.run([5]) == [5]
    assert computer.run([3]) == [8]


def test_several_inputs_in_one_call():
    computer = Computer(RUNNING_TOTAL)
    assert computer.run([1, 2, 3]) == [1, 3, 6]


def test_program_unchanged():
    program = [3, 7, 1001, 7, 1, 7, 99, 0]
    Computer(program).run([41])
    assert program == [3, 7, 1001, 7, 1, 7, 99, 0]


def test_two_computers_are_independent():
    first = Computer(RUNNING_TOTAL)
    second = Computer(RUNNING_TOTAL)
    first.run([10])
    assert second.run([1]) == [1]
    assert first.run([1]) == [11]


def test_relative_mode():
    # outputs its own first number: base = 1, then output the value at base - 1
    assert Computer([109, 1, 204, -1, 99]).run([]) == [109]


def test_relative_base_survives_a_pause():
    # base = 10, read an input into address base + 0, then output the value at address 10
    computer = Computer([109, 10, 203, 0, 4, 10, 99])
    assert computer.run([]) == []
    assert computer.run([42]) == [42]


def test_count_tiles():
    outputs = [1, 2, 3, 6, 5, 4, 0, 0, 3]
    assert count_tiles(outputs, PADDLE) == 2
    assert count_tiles(outputs, BALL) == 1
    assert count_tiles(outputs, BLOCK) == 0


def test_count_tiles_ignores_the_score():
    assert count_tiles([-1, 0, 2, 4, 4, 2], BLOCK) == 1


# ---------------------------------------------------------------- Part 2


def test_game_starts_empty():
    game = ex06.Game()
    assert game.tiles == {}
    assert game.score == 0
    assert game.scores == []


def test_game_update():
    game = ex06.Game()
    game.update([1, 2, 3, 6, 5, 4, -1, 0, 12])
    assert game.tiles == {(1, 2): 3, (6, 5): 4}
    assert game.score == 12
    assert game.scores == [12]


def test_game_update_overwrites():
    game = ex06.Game()
    game.update([1, 2, 4])
    game.update([1, 2, 0, 2, 2, 4])
    assert game.tiles == {(1, 2): 0, (2, 2): 4}
    assert game.scores == [0, 0]


def test_two_games_are_independent():
    first = ex06.Game()
    second = ex06.Game()
    first.update([1, 1, 4, -1, 0, 5])
    assert second.tiles == {}
    assert second.scores == []


def test_ball_and_paddle():
    game = ex06.Game()
    assert game.ball is None
    game.update([0, 0, 1, 3, 4, 4, 2, 7, 3])
    assert game.ball == (3, 4)
    assert game.paddle == (2, 7)
    game.update([3, 4, 0, 4, 5, 4])  # the ball moves
    assert game.ball == (4, 5)
    assert game.paddle == (2, 7)


def test_count():
    game = ex06.Game()
    game.update([0, 0, 2, 1, 0, 2, 1, 0, 0])
    assert game.count(BLOCK) == 1


def test_screen_rows():
    game = ex06.Game()
    game.update([0, 0, 1, 1, 0, 1, 2, 0, 1, 0, 1, 1, 1, 1, 4, 2, 1, 1])
    assert ex06.screen_rows(game) == [[1, 1, 1], [1, 4, 1]]


def test_draw():
    game = ex06.Game()
    game.update([0, 0, 1, 1, 0, 2, 2, 0, 1, 0, 1, 1, 1, 1, 4, 2, 1, 3])
    assert ex06.draw(game) == "#=#\n#o-"


def test_autopilot_chooses_a_joystick_input():
    game = ex06.Game()
    game.update([5, 3, 4, 2, 9, 3])  # ball at x = 5, paddle at x = 2
    assert Autopilot().choose(game) in (-1, 0, 1)


def test_play_stay():
    game = ex06.play(TINY_GAME, Stay())
    assert game.scores == [0, 0, 0, 0]


class Right(Controller):
    def choose(self, game):
        return 1


def test_play_right():
    game = ex06.play(TINY_GAME, Right())
    assert game.score == 3
    assert game.scores == [0, 1, 2, 3]


def test_autopilot_clears_all_blocks():
    game = ex06.play(load_program(PROGRAM_FILE), Autopilot())
    assert game.count(BLOCK) == 0


# ---------------------------------------------------------------- your tests (Part 2)


def test_count_multiple_blocks():
    game = ex06.Game()
    game.update(
        [
            0,
            0,
            BLOCK,
            1,
            0,
            BLOCK,
            2,
            0,
            BALL,
            3,
            0,
            BLOCK,
        ]
    )
    assert game.count(BLOCK) == 3


def test_draw_single_row():
    game = ex06.Game()
    game.update(
        [
            0,
            0,
            WALL,
            1,
            0,
            BLOCK,
            2,
            0,
            BALL,
        ]
    )
    assert ex06.draw(game) == "#=o"
