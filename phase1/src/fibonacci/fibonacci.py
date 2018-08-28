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


errTest="Error: the 'generateFibonacci' function returns {0}, but expected is {1}"

expectedValue=1
length=1
res = generateFibonacci(length)
if res != expectedValue:
    print(errTest.format(res, expectedValue))
    exit(1)

expectedValue=5
length=5
res = generateFibonacci(length)
if res != expectedValue:
    print(errTest.format(res, expectedValue))
    exit(1)

expectedValue=55
length=10
res = generateFibonacci(length)
if res != expectedValue:
    print(errTest.format(res, expectedValue))
    exit(1)

print("The 'generateFibonacci' function check is passed")
