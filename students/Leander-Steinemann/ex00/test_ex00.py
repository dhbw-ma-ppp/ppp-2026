from ex00 import greet


def test_greet():
    assert greet("Ada") == "Hello, Ada!"


def test_greet_another_name():
    assert greet("Grace") == "Hello, Grace!"
