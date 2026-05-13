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
        
def compute_r_of(str, start, stop, beta, p):
    result = 0
    base = 1
    #say we have abc so its index 0,1,2. start is 2 and stop is 0
    for i in range(start, stop-1, -1):
        result = (result + (ord(str[i]) * base)) % p
        base = (beta * base) % p
    return result

def pattern_match(txt, pat):
    m = len(pat)
    n = len(txt)
    BETA = 128
    result = []

    #Find a prime value p so that it can be used to modulate r of pat and portions of txt
    p_value = generate_prime_modulus_p(pat)

    #The r of pat will be used to compare with r portions of txt and if the value are the same we'll need to perform
    #explicit comparisons to see if they match for sure.
    r_of_pat = compute_r_of(pat, m-1, 0,BETA, p_value)

    #Find the first r of txt
    first_r_of_txt = compute_r_of(txt,  m-1, 0, BETA, p_value)

    for i in range(m+1, )
    


print(modular_exponentiation(7,560,561))
# print(generate_prime_modulus_p("abcdefghijklmnop"))
