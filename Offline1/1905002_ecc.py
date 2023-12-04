import math
import random
import numpy as np
import time
from sympy import randprime

def generate_prime_with_bits(bits):
    return randprime(1 << (bits-1), 1 << bits)

def generate_prime_with_digits(n):
    return randprime(10 ** (n-1), 10 ** n)

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


def generate_parameters(p):
    range = p >> 80  # just a random number

    y = 0
    while True:
        y = np.random.randint(-range,range)

        if y !=0: # at singular point, y = 0
            break
    
    x = np.random.randint(-range,range)

    b = 0
    while True:
        a = np.random.randint(-range,range)
        b = (y*y - x*x*x - a*x)

        if ((4*a*a*a + 27*b*b) % p) != 0:
            break

    G = (x,y)

    return a,b,G

    

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

            k_a = random.randint(1<<(key-1), p-1)
            k_b = random.randint(1<<(key-1), p-1)
            
            a = -3
            b = 4
            G = (0, 2)

            # 4*(-3)^3 + 27*4^2 = 324nopass != 0 (mod p) as p is very large and is prime, so the elliptic curve is non-singular

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

if __name__ == "__main__":
    calculate()

