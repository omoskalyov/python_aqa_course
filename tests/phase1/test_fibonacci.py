from src.fibonacci import generateFibonacci, errText


def test_fibonacci1():
    expectedValue = 1
    length = 1
    res = generateFibonacci(length)
    assert expectedValue == res, errText.format(res, expectedValue)


def test_fibonacci2():
    expectedValue = 5
    length = 5
    res = generateFibonacci(length)
    assert expectedValue == res, errText.format(res, expectedValue)


def test_fibonacci3():
    expectedValue = 55
    length = 10
    res = generateFibonacci(length)
    assert expectedValue == res, errText.format(res, expectedValue)

