#!/usr/bin/env python

def generateFibonacci(length):
    """ The function generates Fibonacci sequence.
    Params:
        length - number of numbers
    Output:
        Fibonacci number
    """
    if length < 2:
        return length
    else:
        return generateFibonacci(length - 1) + generateFibonacci(length - 2)


def validateFibonacciFunc(length,expectedValue):
    res = generateFibonacci(length)
    if res != expectedValue:
        print(errText.format(res, expectedValue))
        exit(1)


errText = "Error: the 'generateFibonacci' function returns {0}, but expected is {1}"

if __name__ == "__main__":

    expectedValue = 1
    length = 1
    validateFibonacciFunc(length,expectedValue)

    expectedValue = 5
    length = 5
    validateFibonacciFunc(length,expectedValue)

    expectedValue = 55
    length = 10
    validateFibonacciFunc(length,expectedValue)

    print("The 'generateFibonacci' function check is passed")
