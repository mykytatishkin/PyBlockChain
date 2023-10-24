def isTrue(x):
    # Checks if the input x is equal to 1.
    return x == 1


def if_(i, y, z):
    # Returns y if isTrue(i) is True, otherwise returns z.
    return y if isTrue(i) else z


def and_(i, j):
    # Calls if_ function with i and 0 as arguments, simulating a bitwise AND operation.
    return if_(i, j, 0)


def AND(i, j):
    # Applies the 'and_' function element-wise to the corresponding elements of the input lists i and j.
    return [and_(ia, ja) for ia, ja in zip(i, j)]


def not_(i):
    # Returns 0 if the input i is True, otherwise returns 1.
    return if_(i, 0, 1)


def NOT(i):
    # Applies the 'not_' function element-wise to each element of the input list i.
    return [not_(x) for x in i]


def xor(i, j):
    # Simulates a bitwise XOR operation between i and the NOT of j.
    return if_(i, not_(j), j)


def XOR(i, j):
    # Applies the 'xor' function element-wise to the corresponding elements of the input lists i and j.
    return [xor(ia, ja) for ia, ja in zip(i, j)]


def xorxor(i, j, l):
    # Applies the 'xor' function to i and the result of another 'xor' function between j and l.
    return xor(i, xor(j, l))


def XORXOR(i, j, l):
    # Applies the 'xorxor' function element-wise to the corresponding elements of the input lists i, j, and l.
    return [xorxor(ia, ja, la) for ia, ja, la, in zip(i, j, l)]


def maj(i, j, k):
    # Returns the value with the highest count among i, j, and k.
    return max([i, j], key=[i, j, k].count)


def rotr(x, n):
    # Rotates the list x to the right by n positions.
    return x[-n:] + x[:-n]


def shr(x, n):
    # Shifts the list x to the right by n positions, filling the leftmost positions with zeros.
    return n * [0] + x[:-n]


def add(i, j):
    # Performs a binary addition of lists i and j, considering carry values.
    length = len(i)
    sums = list(range(length))
    c = 0
    for x in range(length - 1, -1, -1):
        sums[x] = xorxor(i[x], j[x], c)
        c = maj(i[x], j[x], c)
    return sums
