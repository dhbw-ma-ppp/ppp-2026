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


# --------------------------------------------------#


def test_opcode_99():
    memory = [99]
    assert step(memory, 0, [], []) is None


def test_opcode_1():
    memory = [1, 5, 6, 0, 0, 10, 20]
    position = step(memory, 0, [], [])

    assert memory[0] == 30
    assert position == 4


def test_opcode_2():
    memory = [2, 5, 6, 0, 0, 10, 20]
    position = step(memory, 0, [], [])

    assert memory[0] == 200
    assert position == 4


def test_opcode_3():
    memory = [3, 3, 0, 0]
    inputs = [42]

    position = step(memory, 0, inputs, [])

    assert memory[3] == 42
    assert inputs == []
    assert position == 2


def test_opcode_4():
    memory = [4, 3, 0, 42]
    outputs = []

    position = step(memory, 0, [], outputs)

    assert outputs == [42]
    assert position == 2


def test_unknown_opcode():
    memory = [42]
    try:
        step(memory, 0, [], [])
        assert False
    except ValueError:
        pass
