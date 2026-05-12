# Ekrithyreach Lay
# Student ID: 33698759
import random

"""
The algorithm computes for a^b mod n in O(logb) time where b is the number of
bits that we need to loop through.
"""
def modular_exponentiation(a, b, n):
    binary_b = bin(b)
    binary_b = binary_b[2:]
    result = 1
    base = a % n
    reversed_binary = binary_b[::-1]
    print(reversed_binary)
    for bit in reversed_binary:
        if bit == '1':
            result = (result * base) % n
        base = (base * base) % n
    return result

"""
The overall algorithmic structure was obtained from the psuedocode provided in Week 6's lecture slides.
We'll assume that n will always be an odd number
"""
def miller_rabin(n, k):
    s = 0
    t = n - 1
    while t % 2 == 0:
        s = s + 1
        t = t//2
    for _ in range(k):
        a = random.randint(2, n-2)
        x = modular_exponentiation(a, t, n)
        if x == 1:
            continue
        for j in range(s):
            prev_x = x
            x = (x * x) % n
            if x == 1:
                if prev_x != n-1:
                    return False
                break
        if x != 1:
            return False
    return True

def generate_prime_modulus_p(pat):
    m = len(pat)
    t = max(32, m)
    # To find the lower and upper bound we can use python's leftward bitshift operation
    # where t represents the number of times we need to shift our bit 1 leftwards. This allows
    # us to bypass the exponent operation in python
    lower_bound = 1 << (t-1)
    upper_bound = (1 << t) - 1
    #This will define the amount of times miller rabin will run for to test different a bases
    k = 32
    while True:
        candidate_number = random.randint(lower_bound, upper_bound)
        result = miller_rabin(candidate_number, k)
        if result == True:
            return candidate_number
        
def compute_r_of_pat(pat, beta, p):
    result = 0
    reverse_pat = pat[::-1]
    for i in range():
        result += 


print(modular_exponentiation(7,560,561))
# print(generate_prime_modulus_p("abcdefghijklmnop"))
print(reversed("abc"))
