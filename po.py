#padding oracle attack
import base64

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import util


class AES_CBC(object):

    def __init__(self, key= get_random_bytes(32)):
        self.key = key
        self._cipher = AES.new(key)

    def _add_padding(self, data):
        padding  = 16 - (len(data) % 16)
        return  data + bytearray([padding  for _ in range(padding)])

    def _split_blocks(self,data):
        blocks = []
        l = len(data)
        for i in range(0, l / 16):
            blocks.append(data[ (i *  16): (i +  1) * 16])
        return blocks

    def _strip_and_check_padding(self, data):
        data = bytearray(data)
        expected_padding  = data[-1]

        for byte in data[len(data)  - expected_padding:]:
            if expected_padding ==  0 or expected_padding > 16:
                raise ValueError("Incorrect Padding!")
            if  byte != expected_padding:
                raise ValueError("Incorrect Padding!")
        return str(data[ :len(data) - expected_padding])


    def encrypt(self ,plaintext):
        plaintext = self._add_padding(bytearray(plaintext))
        plaintext_blocks = self._split_blocks(plaintext)

        #initiatilization vector
        iv = get_random_bytes(16)


        cipher_blocks = []
        for i, block in enumerate(plaintext_blocks):
            if (i == 0):
                cipher_blocks.append(iv)
                cipher_blocks.append(self._cipher.encrypt(str(util.xor(iv,block))))
            else:
                cipher_blocks.append(self._cipher.encrypt(str(util.xor(cipher_blocks[i],block))))

        return base64.b64encode(''.join(cipher_blocks))


    def decrypt(self ,ciphertext):
        ciphertext = bytearray(base64.b64decode(ciphertext))
        ciphertext_blocks = self._split_blocks(ciphertext)

        plaintext_blocks = []

        for i, block in enumerate(ciphertext_blocks):
            if i == 0:
                continue
            plaintext_blocks.append(str(util.xor(self._cipher.decrypt(str(block)), ciphertext_blocks[i-1])))

        return self._strip_and_check_padding(''.join(plaintext_blocks))
