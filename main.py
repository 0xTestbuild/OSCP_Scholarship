from po import AES_CBC
import pdb

if __name__ == "__main__":
    print "Padding attack tutorial program started...!"


    cipher = AES_CBC()
    cipher_text  = cipher.encrypt( "a" * 16  +  "bbbbbb")
    pdb.run("cipher.decrypt(cipher_text)")
    # plain_text = cipher.decrypt(cipher_text)

    print "ciper_text:"
    print cipher_text
    print ""
    print "plain_text:"
    print plain_text
