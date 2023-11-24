import math
import random
import time
from sympy import randprime

def generate_prime_with_bits(bits):
    return randprime(1 << (bits-1), 1 << bits)

# computes n^x % p
def modulo_power(n, x, p):
    if x == 0:
        return 1
    
    m = modulo_power(n, x//2 , p) % p
    m = (m*m) % p

    if (x % 2) == 0:
        return m
    
    return (n * m) % p


# generates modulo inverse of n mod p on the assumption that gcd(n,p) = 1
# uses fermat's little theorem
# n^(p-1) = 1 (mod p) ==> n'n^(p-1) = n' (mod p) ==> n^(p-2) = n' (mod p) 
def modulo_inverse(n,p):
    return modulo_power(n, p-2, p)

def point_addition(P, Q, p):
    (x1,y1) = P
    (x2,y2) = Q

    m = (y2 - y1) % p
    s = (m * modulo_inverse(x2 - x1, p)) % p

    x = (((s * s) % p) - x1 - x2) % p
    y = (((s * (x1 - x)) % p) - y1) % p

    return (x,y)

def point_doubling(P, a, p):
    (x1,y1) = P

    m = (3*x1*x1 + a) % p
    s = (m * modulo_inverse(2*y1, p)) % p

    x = (((s * s) % p) - x1 - x1) % p
    y = (((s * (x1 - x)) % p) - y1) % p

    return (x,y)

# calculates nP
def multiply_point(P, n, a, p):
    if n == 1:
        return P
    
    t = int(math.log2(n)) - 1

    Q = P
    while t >= 0:
        Q = point_doubling(Q, a, p)
        if (n & (1 << t)) != 0:
            Q = point_addition(Q, P, p)
        t -= 1
    return Q


def calculate():
    # 128 digit prime
    n_iteration = 5
    print("k \t\t A \t\t\t B \t\t\t R")

    for key in [128, 192, 256]:
        print(key, end = "\t") 

        time_taken_A = 0
        time_taken_B = 0
        time_taken_R = 0
        for _ in range(1, n_iteration):      
            p = generate_prime_with_bits(key)

            k_a = p - (1 << 20) * random.randint(1,1000)
            k_b = p - (1 << 20) * random.randint(1,1000)
            
            a = -3
            b = 4
            G = (2, 7)

            start = time.time()
            # print(k_a , end = "\t")
            A = multiply_point(G, k_a, a, p)
            time_taken_A += time.time() - start

            start = time.time()
            B = multiply_point(G, k_b, a, p)
            time_taken_B += time.time() - start

            start = time.time()
            R = multiply_point(A, k_b, a, p)
            time_taken_R += time.time() - start

        print(time_taken_A * 1000 / n_iteration, end = "\t")
        print(time_taken_B * 1000 / n_iteration, end = "\t")
        print(time_taken_R * 1000 / n_iteration, end = "\t")
        print()


calculate()

# print(modulo_inverse(2, 17))

# 16 digit prime
# prime = 8735839625367917

# prime = 113

# # code starts here
# # the elliptic curve is y^2 = x^3 - 3x + 4
# a = -3
# b = 4

# p = prime
# G = (2, 7)

# # both alice and bob have agreed on the values of a, b, p, G

# # E is the order of the elliptic curve
# E = p + 1 - 2 * int(math.sqrt(p))

# start = time.time()

# # alice code
# # alice's private key
# k_a = random.randint(2, E-1)
# # alice's public key
# A = multiply_point(G, k_a, a, p)


# # bob code
# k_b = random.randint(2, E-1)
# B = multiply_point(G, k_b, a, p)

# # alice sends A to bob
# # bob sends B to alice

# # alice computes k_aB
# k_aB = multiply_point(B, k_a, a, p)

# # bob computes k_bA
# k_bA = multiply_point(A, k_b, a, p)

# time_taken = time.time() - start

# print("Time taken: ", time_taken * 1000, "ms")

# print("Alice ", k_aB)
# print("Bob ", k_bA)

# for i in range(1,19):
#     print(i, end ="")
#     print("P: ", multiply_point((5,1), i, 2, 17))

