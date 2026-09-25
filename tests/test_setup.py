import sys


def test_python_version():
    assert sys.version_info >= (3, 14), f"expected Python 3.14 or newer, got {sys.version}"


def test_pytest_works():
    assert 1 + 1 == 2
