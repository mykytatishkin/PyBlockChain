# Import necessary functions and constants from external modules
from Utils.helper import b2Tob16, preprocessMessage, chunker, initializer
from Utils.utils import *
from Utils.constants import *


# Define a function for SHA-256 hashing
def sha256(message):
    # Initialize the constants used in the SHA-256 algorithm
    k = initializer(K)
    h0, h1, h2, h3, h4, h5, h6, h7 = initializer(h_hex)

    # Break the input message into smaller chunks for processing
    chunks = preprocessMessage(message)

    # Iterate through each chunk
    for chunk in chunks:
        # Break the chunk into 32-bit words
        w = chunker(chunk, 32)

        # Expand the word list to 64 words as required by SHA-256
        for _ in range(48):
            w.append(32 * [0])

        # Initialize variables to store the current hash values
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        # Perform the core SHA-256 computation for each word
        for j in range(64):
            S1 = XORXOR(rotr(e, 6), rotr(e, 11), rotr(e, 25))
            ch = XOR(AND(e, f), AND(NOT(e), g))
            temp1 = add(add(add(add(h, S1), ch), k[j]), w[j])
            S0 = XORXOR(rotr(a, 2), rotr(a, 13), rotr(a, 22))
            m = XORXOR(AND(a, b), AND(a, c), AND(b, c))
            temp2 = add(S0, m)

            # Update hash values for the next iteration
            h = g
            g = f
            f = e
            e = add(d, temp1)
            d = c
            c = b
            b = a
            a = add(temp1, temp2)

        # Update the hash values for this chunk
        h0 = add(h0, a)
        h1 = add(h1, b)
        h2 = add(h2, c)
        h3 = add(h3, d)
        h4 = add(h4, e)
        h5 = add(h5, f)
        h6 = add(h6, g)
        h7 = add(h7, h)

    # Generate the final SHA-256 hash digest as a hexadecimal string
    digest = ''
    for val in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += b2Tob16(val)

    return digest


# Entry point for the program
if __name__ == '__main__':
    verdict = 'y'

    # Loop to allow the user to input messages and compute their SHA-256 hashes
    while verdict == 'y':
        input_message = input('Type or copy your message here: ')
        print('Your message: ', input_message)
        print('Hash: ', sha256(input_message))
        verdict = input('Do you want to try another text? (y/n): ').lower()
