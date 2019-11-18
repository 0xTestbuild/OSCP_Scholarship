def xor(ba1, ba2):
    """ XOR two byte arrays"""
    ba1 = bytearray(ba1)
    ba2 = bytearray(ba2)
    return bytearray([ba1[i] ^ ba2[i] for i in range(0, len(ba1))])
