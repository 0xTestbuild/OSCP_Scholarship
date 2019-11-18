import util
import base64
from Crypto.Random import get_random_bytes
from po import AES_CBC
from Crypto.Cipher import AES
import pdb

global_cipher =  AES_CBC()

def split_blocks(data):
    blocks = []
    l = len(data)
    for i in range(0, l / 16):
        blocks.append(data[ (i *  16): (i +  1) * 16])
    return blocks

def find_last_byte(cipher_text):
    cipher_text = bytearray(base64.b64decode(cipher_text))

    # print"cipher_text"
    # print cipher_text
    # print ""

    blocks = split_blocks(cipher_text)

    # print "blocks"
    # print blocks
    # print ""

    arr = [b for b in blocks[0]]
    print arr

    c_prime = bytearray([b for b in blocks[0]])


    # print c_prime
    # print ""

    plain_text_bytes  = bytearray([0 for _ in range(16)])

    for i in range(16):

        expected_padding = bytearray([0 for _ in range( 16 -  i)] + [(i+1) for _ in range(i)])
        ep = [0 for _ in range( 16 -  i)] + [(i+1) for _ in range(i)]
        print ep
        # print [0 for _ in range( 16 -  i)] + [(i+1) for _ in range(i)]

        c_prime = util.xor(util.xor(expected_padding, plain_text_bytes) , blocks[0])

        # print c_prime

        for byte in range(blocks[0][15 - i] + 1, 256) + range(0, blocks[0][15 - i] + 1):
            c_prime[15 -i] = byte

            to_test = base64.b64encode(str(c_prime + blocks[1]))

            try:
                global_cipher.decrypt(to_test)
                print global_cipher.decrypt(to_test)
                print  " At i == " + str(i)  + " encode found at byte = "+ str(byte)
                #print global_cipher.decrypt(to_test)
                plain_text_bytes[15-i] =  (byte ^ (i+1) ^ blocks[0][15 -i])
                break
            except:
                pass
    return  "PO Attack Decryption: " + "".join([chr(b) for b in plain_text_bytes])



if __name__ == "__main__":
    plain_text = "abcdefghijklmno"
    cipher_text  = global_cipher.encrypt(plain_text)

    print "encoded:\n" + cipher_text

    # pdb.run("find_last_byte(cipher_text)")

    print find_last_byte(cipher_text)
    # ba = bytearray([0 for _ in range(16)])
    # for i in range(1,17):
    #     ba[i] = str(global_cipher._add_padding(str(bytearray(get_random_bytes(chr(1))))))
