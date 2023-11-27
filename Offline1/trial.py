# Python 3 implementation of the approach
from math import sqrt, pow
sz = 100005
isPrime = [True for i in range(sz + 1)]
 
# Function for Sieve of Eratosthenes
def sieve():
    isPrime[0] = isPrime[1] = False
 
    for i in range(2, int(sqrt(sz)) + 1, 1):
        if (isPrime[i]):
            for j in range(i * i, sz, i):
                isPrime[j] = False
 
# Function to print all the prime
# numbers with d digits
def findPrimesD(d):
     
    # Range to check integers
    left = int(pow(10, d - 1))
    right = int(pow(10, d) - 1)
 
    # For every integer in the range
    for i in range(left, right + 1, 1):
         
        # If the current integer is prime
        if (isPrime[i]):
            print(i, end = " ")
         
# Driver code
if __name__ == '__main__':
     
    print(chr(8))
     
# This code is contributed by Surendra_Gangwar