import random, sys

#pregenerated primes
first_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 
                 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 
                 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 
                 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,317, 331, 337, 347, 349, 353, 
                 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 
                 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 
                 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 
                 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 
                 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 
                 953, 967, 971, 977, 983, 991, 997]

def gcd(a, b):
    if (a == 0):
        return b

    return gcd(b % a, a)

#iterative method to find mod inverse
def findModInverse(a, m):
    if (m == 1):
        return 0
    
    m0, y, x = m, 0, 1
    while (a > 1):
        # q is quotient
        q = a // m
        t = m
        m = a % m
        a = t
        t = y
        # Update x and y
        y = x - q * y
        x = t

    # Make x positive
    if (x < 0):
        x = x + m0
    return x

def rabinMillerTest(num):
    maxDivisionsByTwo = 0
    ec = num-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == num-1)
 
    def trialComposite(round_tester):
        if pow(round_tester, ec, num) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, num) == num-1:
                return False
        return True
 
    # Set number of trials here
    numberOfRabinTrials = 10
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, num)
        if trialComposite(round_tester):
            return False
    return True

def isPrime(num):
    if (num < 2):
        return False

    for prime in first_primes: 
            #check if there is a prime in first_primes that divides num
            if num % prime == 0 and prime**2 <= num:
                return False
            else:
                return True

def generateLargePrime(keysize = 1024):
    #We first pick a random number with a desired bit-size
    while True:
        num = random.randrange(2**(keysize-1)+1, 2**(keysize))
        if isPrime(num): 
            # If no small primes divide num, run Rabin-Miller test
            if not rabinMillerTest(num):
                continue #Generate a new random number if Rabin-Miller test fails
            else:
                return num

def generateKeys(keySize):
    p = generateLargePrime(keySize)
    q = generateLargePrime(keySize)
 
    n = p * q
    totient = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if gcd(e, totient) == 1:
            break

    d = findModInverse(e, totient)

    publicKey = (n, e)
    privateKey = (n, d)
    return (publicKey, privateKey)

def genKeyFiles(user, keySize):
    publicKey, privateKey = generateKeys(keySize)

    pubFile = open('%s.pub' % (user), 'w+')
    pubFile.write('%s,%s' % (publicKey[0], publicKey[1]))
    #publicKey[0] is n and publickey[1] is e
    pubFile.close()

    prvFile = open('%s.prv' % (user), 'w+')
    prvFile.write('%s,%s' % (privateKey[0], privateKey[1]))
    #privateKey[0] is n and privateKey[1] is d
    prvFile.close()

if __name__ == '__main__':
    Keysize = 1024
    userName = sys.argv[1]
    genKeyFiles(userName, Keysize)

