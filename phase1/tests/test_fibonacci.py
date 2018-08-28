from fibonacci import generateFibonacci


def test_fibonacci1():
    a = 1
    assert generateFibonacci(1) == 1


def test_fibonacci2():
    assert generateFibonacci(5) == 5


def test_fibonacci3():
    assert 55 == generateFibonacci(10), "Error: the 'generateFibonacci' function returns {0}, but expected is {1}"

