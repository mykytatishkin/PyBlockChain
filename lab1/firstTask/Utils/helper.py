# To do hash function SHA-256, we need to know what is data types, like binary, hexadecimal, decimal, etc.
# So we need to create from Word num, so in python we have function ord(),
# example: ord('H') -> 72, and now we can make bin num, bin(72) -> '0b1001000'
#
# Where ‘0b’ lets Python know it’s a binary string. So we will have to chop this indicator off,
# and then we are left with 7 bits. We thus need to prepend another zero. And finally,
# we will cast each character to an integer.
# The bellow function takes care of all the conversions and returns a list of zeros and ones.
def translate(message):
    charcodes = [ord(c) for c in message]
    bytes = []
    for char in charcodes:
        bytes.append(bin(char)[2:].zfill(8))
        # bin(char)[2:]: This part of the code slices the binary string to remove the '0b' prefix,
        # so you're left with just the binary representation. In the example of bin(65), this would yield '1000001'.

        # zfill(8): The zfill() method is used to pad the binary string with leading zeros (if necessary) to ensure
        # it's 8 characters long. This is done because ASCII characters are typically represented using 8 bits (1 byte).
        # For example, if the binary string is '1000001', it doesn't need padding.
        # But if it's '101', it will be padded to '00000101'.

    bits = []
    for byte in bytes:
        for bit in byte:
            bits.append(int(bit))
    return bits


def chunker(bits, chunk_length=8):
    # divides list of bits into desired byte/word chunks,
    # starting at LSB
    chunked = []
    for b in range(0, len(bits), chunk_length):
        chunked.append(bits[b:b + chunk_length])
    return chunked


# To be able to accommodate both our needs of set bit lengths and utilizing the built-in Python functions,
# as well as being able to conveniently fill words with zeros,
# we’ll us the below utility function to simply append or prepend a required number of zeros to a list.
def fillZeros(bits, length=8, endian='LE'):
    l = len(bits)
    if endian == 'LE':
        for i in range(l, length):
            bits.append(0)
    else:
        while l < length:
            bits.insert(0, 0)
            l = len(bits)
    return bits


def preprocessMessage(message):
    # translate message into bits
    bits = translate(message)
    # message length
    length = len(bits)
    # get length in bits  of message (64 bit block)
    message_len = [int(b) for b in bin(length)[2:].zfill(64)]
    # if length smaller than 448 handle block individually otherwise
    # if exactly 448 then add single 1 and add up to 1024 and if longer than 448
    # create multiple of 512 - 64 bits for the length at the end of the message (big endian)
    if length < 448:
        # append single 1
        bits.append(1)
        # fill zeros little endian wise
        bits = fillZeros(bits, 448, 'LE')
        # add the 64 bits representing the length of the message
        bits = bits + message_len
        # return as list
        return [bits]
    elif 448 <= length <= 512:
        bits.append(1)
        # moves to next message block - total length = 1024
        bits = fillZeros(bits, 1024, 'LE')
        # replace the last 64 bits of the multiple of 512 with the original message length
        bits[-64:] = message_len
        # returns it in 512 bit chunks
        return chunker(bits, 512)
    else:
        bits.append(1)
        # loop until multiple of 512 + 64 bit message_len if message length exceeds 448 bits
        while (len(bits) + 64) % 512 != 0:
            bits.append(0)
        # add the 64 bits representing the length of the message
        bits = bits + message_len
        # returns it in 512 bit chunks
        return chunker(bits, 512)


def initializer(values):
    # convert from hex to python binary string (with cut bin indicator ('0b'))
    binaries = [bin(int(v, 16))[2:] for v in values]
    # convert from python string representation to a list of 32 bit lists
    words = []
    for binary in binaries:
        word = []
        for b in binary:
            word.append(int(b))
        words.append(fillZeros(word, 32, 'BE'))
    return words


# It`s can be, but not mandatory, that the hash value is presented in hexadecimal notation, like SHA-256
# So we need a function to convert from bin to hex
def b2Tob16(value):
    value = ''.join([str(x) for x in value])  # we are making string from value,
    # if we have [0, 1, 1, 0, 1, 0, 1, 1] we will get '01101011'
    # creat 4 bit chunks, and add bin-indicator
    binaries = []
    for d in range(0, len(value), 4):
        binaries.append('0b' + value[d:d + 4])
    # transform to hexadecimal and remove hex-indicator
    hexes = ''
    for b in binaries:
        hexes += hex(int(b, 2))[2:]
    return hexes
