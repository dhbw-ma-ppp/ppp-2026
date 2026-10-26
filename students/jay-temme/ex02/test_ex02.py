from ex02 import find_noun_verb, run, run_with, step

# ---------------------------------------------------------------- Part 1


def test_step_add():
    memory = [1, 0, 0, 0, 99]
    assert step(memory, 0) == 4
    assert memory == [2, 0, 0, 0, 99]


def test_step_multiply():
    memory = [2, 3, 0, 3, 99]
    assert step(memory, 0) == 4
    assert memory == [2, 3, 0, 6, 99]


def test_step_at_a_later_position():
    memory = [1, 0, 0, 0, 2, 4, 4, 0, 99]
    assert step(memory, 4) == 8
    assert memory == [4, 0, 0, 0, 2, 4, 4, 0, 99]


def test_step_halt():
    assert step([99], 0) is None


def test_run():
    assert run([1, 5, 6, 0, 99, 20, 22]) == 42


def test_run_reads_what_it_wrote():
    assert run([2, 9, 10, 9, 1, 9, 11, 0, 99, 6, 7, 3]) == 45


def test_run_changes_its_own_program():
    # the first instruction writes 99 to position 4
    assert run([1, 9, 10, 4, 1, 0, 0, 0, 99, 50, 49]) == 1


# input:            memory = [1, 0, 0], position = 0
# expected output:  function raises a ValueError
# case:             memory does not have enough indecies to properly execute an opcode
def test_step_wrong_memory_length():
    try:
        step([1, 0, 0], 0)
        assert False
    except IndexError:
        assert True


# input:            memory = [3], position = 0
# expected output:  function raises a ValueError
# case:             memory contains a not implemented opcode
def test_step_unknown_opcode():
    try:
        step([3], 0)
        assert False
    except ValueError:
        assert True


# input:            step([1, 0, 0, 999, 99],0)
# expected output:  ValueError "Output index is out of bounds"
# case:             999 is not in the range of the list.
def test_step_index_out_of_bounds():
    try:
        step([1, 0, 0, 999, 99], 0)
        assert False
    except ValueError:
        assert True


# input:            program = [1, 0, 0, 4, 0, 3, 0, 0, 99]
# expected output:  4
# case:             the program writes the opcode it's going to execute next
def test_run_writes_opcode():
    assert run([1, 0, 0, 4, 0, 3, 0, 0, 99]) == 4


# ---------------------------------------------------------------- Part 2
# Add at least two tests of your own below, for the Part 2 functions.

# computes 100 * noun + verb
HUNDRED_NOUN_PLUS_VERB = [1, 0, 0, 3, 2, 1, 13, 13, 1, 13, 2, 0, 99, 100] + [0] * 86


def test_run_with():
    assert run_with(HUNDRED_NOUN_PLUS_VERB, 12, 34) == 1234


def test_find_noun_verb():
    assert find_noun_verb(HUNDRED_NOUN_PLUS_VERB, 1234) == (12, 34)


# input:            program = [99, 0, 0], noun = "test", verb = 0
# expected output:  function raises a TypeError
# case:             noun or verb are not integers
def test_run_with_noun_is_not_int():
    try:
        run_with([99, 0, 0], "test", 0)
        assert False
    except TypeError:
        assert True


# input:            program = [99], noun = 0, verb = 0
# expected output:  99
# case:             program is not long enough to simply insert noun and verb
def test_run_with_program_length_is_1():
    assert run_with([99], 0, 0) == 99


# input:            program = [1, 0, 0, 3, 99] + [0] * 95, target = 0
# expected output:  None
# case:             no noun and verb can cause program to return target
def test_find_noun_verb_impossible():
    assert find_noun_verb([1, 0, 0, 3, 99] + [0] * 95, 0) is None
