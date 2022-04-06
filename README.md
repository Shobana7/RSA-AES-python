The aim is to implement a system that uses AES to encrypt data and RSA to protect AES keys.

● Genkeys.py:
This python program is used to generate the public and private keys of the user. It takes as input the name of the user from the common line. The output of the program is two files .prv and .pub containing the private and public keys respectively.

The RSA key generation implementation starts with the generation of large prime numbers p and q. To generate such large numbers, we first pick a random number of desired bit size. We then check if any of the first few primes divide the chosen random number. If yes, we pick a new random number. If not, we pass that number to the Rabin-Miller primality test. If the number passes the Rabin-Miller test then it is our large prime else we choose a different random number and follow these steps again.
With p and q, we compute N and totient. We then select a random number that is relatively prime to the totient. N along with this result will be our user’s public key. We then find the modular inverse of the result. This will constitute the user’s private key along with N. The output is written to files.
 
Commands to run the program:
             
             python3 genkeys.py alice
             
● Crypt.py:
This python program will encrypt or decrypt according to the input command. It uses an argument parser to choose between encryption and decryption.

Encryption:
A 16 bytes random number is chosen as the AES key. This key is used to encrypt the
plain text using the AES-128 algorithm. It imports pyaes module for this purpose.
The AES key is encrypted using the RSA algorithm using the user’s public key. Both
the ciphertext and the encrypted AES key are written to the .cip output file.

Decryption:
The ciphertext and the encrypted AES key are read from the .cip file along with the
user’s private key from the .prv file. RSA is first run with the private key to decrypt the encrypted AES key. This gives us the AES key to decrypt the ciphertext. The resulting plaintext is written to a file.

Commands to run the program:
             
             python3 crypt.py -e alic.pub message.txt secret.cip
             python3 crypt.py -d alice.prv secret.cip plaintext.txt
