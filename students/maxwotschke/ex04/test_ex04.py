import pytest

from ex04 import (
    MAX_OF_TWO,
    PROGRAM_FILE,
    decode,
    load_program,
    parameter,
    parse_program,
    run,
    step,
)

# ---------------------------------------------------------------- Part 1


def test_parse_program_one_line():
    assert parse_program("1,0,0,0,99") == [1, 0, 0, 0, 99]


def test_parse_program_spaces_and_negative_numbers():
    assert parse_program(" 1101, 100, -1, 4, 0 ") == [1101, 100, -1, 4, 0]


def test_parse_program_lines_and_comments():
    text = "# adds two numbers\n\n1, 5, 6, 0    # 0: add\n99  # 4: halt\n20, 22\n"
    assert parse_program(text) == [1, 5, 6, 0, 99, 20, 22]


def test_load_program():
    assert load_program(PROGRAM_FILE)[:4] == [3, 190, 1, 190]


def test_decode():
    assert decode(1002) == (2, [0, 1, 0])
    assert decode(104) == (4, [1, 0, 0])
    assert decode(99) == (99, [0, 0, 0])


def test_parameter():
    memory = [1002, 4, 3, 4, 33]
    assert parameter(memory, 0, 1) == 33
    assert parameter(memory, 0, 2) == 3


def test_step_multiply_with_modes():
    memory = [1002, 4, 3, 4, 33]
    assert step(memory, 0, [], []) == 4
    assert memory == [1002, 4, 3, 4, 99]


def test_step_negative_numbers():
    memory = [1101, 100, -1, 4, 0]
    assert step(memory, 0, [], []) == 4
    assert memory == [1101, 100, -1, 4, 99]


def test_step_input():
    memory = [3, 0, 99]
    inputs = [7, 8]
    assert step(memory, 0, inputs, []) == 2
    assert memory == [7, 0, 99]
    assert inputs == [8]


def test_step_output():
    outputs = []
    assert step([4, 2, 99], 0, [], outputs) == 2
    assert step([104, 5, 99], 0, [], outputs) == 2
    assert outputs == [99, 5]


def test_step_halt():
    assert step([99], 0, [], []) is None


def test_step_unknown_opcode():
    with pytest.raises(ValueError):
        step([42, 0, 0, 0], 0, [], [])


def test_run_echo():
    assert run([3, 0, 4, 0, 99], [42]) == [42]


def test_run_does_not_change_inputs():
    inputs = [42]
    run([3, 0, 4, 0, 99], inputs)
    assert inputs == [42]


def test_run_exercise_02_program():
    memory = [1, 5, 6, 0, 99, 20, 22]
    assert run(memory, []) == []
    assert memory[0] == 42


# ---------------------------------------------------------------- Part 2
# Add at least two tests of your own below, for the Part 2 opcodes.


def test_step_jump_if_true():
    assert step([1105, 1, 7], 0, [], []) == 7
    assert step([1105, 0, 7], 0, [], []) == 3


def test_step_jump_if_false():
    assert step([1106, 0, 7], 0, [], []) == 7
    assert step([1106, 1, 7], 0, [], []) == 3


def test_step_less_than():
    memory = [1107, 1, 2, 5, 99, -1]
    assert step(memory, 0, [], []) == 4
    assert memory[5] == 1


def test_step_equals():
    memory = [8, 5, 6, 7, 99, 3, 3, -1]
    assert step(memory, 0, [], []) == 4
    assert memory[7] == 1


def test_run_max_of_two():
    assert run(MAX_OF_TWO.copy(), [3, 8]) == [8]


def test_negative_opcode():
    with pytest.raises(ValueError):
        run([-102, 2, 3, 4, 99], [])


def test_run_empty_inputs():
    memory = [3, 1, 4, 0, 99]
    assert step(memory, 0, [], []) == 2
    assert memory == [3, 1, 4, 0, 99]


def test_run_without_inputs():
    with pytest.raises(ValueError):
        run([], [])
