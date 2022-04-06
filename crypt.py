import os, pyaes, sys, argparse

def AES_encrypt(plain_text,aes_key):  
    cipher_text = pyaes.AESModeOfOperationCTR(aes_key).encrypt(plain_text)
    return cipher_text

def RSA_encrypt(aes_key,N,e):
    p = int.from_bytes(aes_key, sys.byteorder)
    e, N = int(e), int(N)
    cipher_key = pow(p, e, N)
    cipher_key = bytes(str(cipher_key).encode())
    return cipher_key

def RSA_decrypt(cipher_key,d,N):
    cipher_key, d, N = int(cipher_key), int(d), int(N)
    aes_key = pow(cipher_key, d, N)
    return aes_key

def AES_decrypt(cipher_text,aes_key):
    aes = pyaes.AESModeOfOperationCTR(aes_key.to_bytes(16, sys.byteorder))
    decrypted = aes.decrypt(cipher_text)
    return decrypted

def encrypt_RSA_AES(pub_key, plain_text, secret_cip):
    N, e = open(pub_key, 'r').read().split(',')
    plain_text = open(plain_text, 'rb').read()

   #Random AES key generation
    aes_key = os.urandom(16)  

    #encrypt data using AES 
    cipher_text = AES_encrypt(plain_text,aes_key)  
    
    #encrypt key using RSA
    cipher_key = RSA_encrypt(aes_key,N,e)

    #writing to file
    secret_file = open(secret_cip, 'wb')
    secret_file.write(b'%b %b' % (cipher_text, cipher_key))
    secret_file.close()


def decrypt_RSA_AES(prv_key, secret_cip, plain_text):
    N, d = open(prv_key, 'r').read().split(',')
    secret = open(secret_cip, 'rb').read().split(b' ')
    cipher_text = b' '.join(secret[:-1])
    cipher_key = secret[-1]

    #decrypting the encrypted key using RSA
    aes_key = RSA_decrypt(cipher_key,d,N)

    #decrypting the encrypted data using AES
    decrypted = AES_decrypt(cipher_text,aes_key)

    #writing to file
    plain_text_file = open(plain_text, 'wb')
    plain_text_file.write(decrypted)
    plain_text_file.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #Reqd arguments for commandline
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", help="Encryption")
    group.add_argument("-d", help="Decryption")

    parser.add_argument("inputFile", help="Source File")
    parser.add_argument("outputFile", help="Destination File")

    args = parser.parse_args()

    if args.e:
        encrypt_RSA_AES(args.e, args.inputFile, args.outputFile)
    elif args.d:
        decrypt_RSA_AES(args.d, args.inputFile, args.outputFile)