# Ekrithyreach Lay
# Student ID: 33698759

import random
import sys

#############################
#   Modular Exponentiation
#############################
def modular_exponentiation(a, b, n):
    """
    The algorithm computes for a^b mod n in O(logb) time where b is the number of
    bits that we need to loop through.
    """
    binary_b = bin(b)
    # Using the bin command would cause the binary value to have 0x at the front
    # So I'll do a list slicing to remove it
    binary_b = binary_b[2:]
    result = 1
    base = a % n
    reversed_binary = binary_b[::-1]
    # As we're looping from left to right the binary needs to be reversed in order
    # to get the correct base and result
    for bit in reversed_binary:
        if bit == '1':
            result = (result * base) % n
        base = (base * base) % n
    return result

######################
#    Miller Rabin
######################
def miller_rabin(n, k):
    """
    The overall algorithmic structure was obtained from the psuedocode provided in Week 6's lecture slides.
    We'll assume that n will always be an odd number
    """
    s = 0
    t = n - 1
    #This loop keeps going until t becomes an odd number
    while t % 2 == 0:
        s = s + 1
        t = t//2
    for _ in range(k):
        a = random.randint(2, n-2)
        x = modular_exponentiation(a, t, n)
        # If x_0 is 1 then this means that any subsequent x_1, x_2,...,x_s and so on would yield 1 as well so we can
        # skip and continue with the next iteration instead.
        if x == 1:
            continue
        for j in range(1, s+1):
            prev_x = x
            x = (x * x) % n
            # This means that we have encountered our first 1 in x_i
            if x == 1:
                # To ensure that n is possibly a prime number we'll need to check if x_i-1 is congruent to -1(n-1).
                # if not then we know for sure that n is not a prime number and can immediatly return false
                if prev_x != n-1:
                    return False
                # We'll end the for loop prematurely here as x_i+1, x_i+2, ... , x_s would be 1 anyways
                break
        # After running the for loop we'll have x_s which is equivalent to doing a^n-1 mod n and if the value is different
        # from 1 then we know for sure its composite
        if x != 1:
            return False
    return True

########################################
#   Generating a random prime number
########################################
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
    """
    A Helper function used to compute the r value of a string in the given portion string[stop...start]. 
    We'll loop from right to left where results from the previous characters will be used to find the result
    with the current character. 
    
    eg say we have string doggo with start=2 and end=0 which corresponds to the string dog. During the for loop
    we'll get the r of g, then r of og, then r of dog.
    """
    result = 0
    base = 1
    #say we have abc so its index 0,1,2. start is 2 and stop is 0
    for i in range(start, stop-1, -1):
        result = (result + (ord(str[i]) * base)) % p
        base = (beta * base) % p
    return result

##############################################
#   Pattern matching by hashing and checking
##############################################
def pattern_match(txt, pat):
    """
    The pattern matching algorithm would determine the r value of the pattern first and afterwards we'll determine
    the r values of each portion within the txt and if a certain portion has the same r value as pat then we'll do
    explicit comparisons to ensure that they truly match each other.
    """
    m = len(pat)
    n = len(txt)
    BETA = 128
    result = []

    # its not possible for the pat to match with the text if it's length exceeds it
    # so we'll return nothing
    if m > n:
        return []

    #Find a prime value p so that it can be used to modulate r of pat and portions of txt
    p_value = generate_prime_modulus_p(pat)

    #The r of pat will be used to compare with r portions of txt and if the value are the same we'll need to perform
    #explicit comparisons to see if they match for sure.
    r_of_pat = compute_r_of(pat, m-1, 0,BETA, p_value)
    first_r_of_txt = compute_r_of(txt,  m-1, 0, BETA, p_value)

    if first_r_of_txt == r_of_pat:
        for index in range(m):
            if txt[index] != pat[index]:
                break
        result.append(0) # The hash value of the text is equal to the hash value of the first portion of txt and the characters
                         # match each other as well.

    curr_r_txt = first_r_of_txt    
    beta_m_minus_one = modular_exponentiation(BETA,m-1,p_value)

    # We'll need to start from m onwards as it'll be the end point for the txt portion that we'll use to compute for the
    # next r value of txt.
    for i in range(m, n):

        # Say we have a string abcdefgh and the length of pat is 4, that means we'll need to find r of abcd, bcde, cdef etc...
        # In the naive approach as we'll be forced to recompute the r values for each each sliding window without taking into
        # account the previous r_value

        # In the optimised approach below the idea is that say we already computed r for abcd and now we need to compute r
        # for bcde. We can see that the suffix bcd of abcd, exists within the prefix of bcde. With this we can determine
        # r of bcde with the optimisation below

        # r_of_abcd = ((a * Beta^3) + (b * Beta^2) + (c * Beta^1) + d) mod p
        # r_of_abcd_without_a = r_of_abcd - (a * Beta^3)

        # We can easily compute for Beta^3 with our modular exponentiation function which we'll only need to compute
        # for once

        # r_of_bcde = (r_of_abcd_without_a * Beta) + e) mod p

        val_of_first_char_removed = ord(txt[i-m]) * beta_m_minus_one
        r_of_first_char_removed = curr_r_txt - val_of_first_char_removed
        curr_r_txt = ((r_of_first_char_removed * BETA) + ord(txt[i])) % p_value
        if curr_r_txt == r_of_pat:
            for index in range(m):
                if txt[i-m+1+index] != pat[index]:
                    break
            result.append(i-m+1) # Perform explicit pattern matching with the portion of the text just the one like above 
                                 # if they have the same r value.
    return result

# The overall code has been obtained from the Command-line usage tutorial for Assignments
# with the modification with the readlines() to readline() as the pattern and text txt files 
# only contain stuff in the first line.
def read_file(file_path: str) -> str:
    f = open(file_path, 'r')
    line = f.readline()
    f.close()
    return line

# The overall code has been obtained from the Command-line usage tutorial for Assignments
if __name__ == '__main__':
    #retrieve the file paths from the commandline arguments
    _, filename1, filename2 = sys.argv

    txt = read_file(filename1)
    pat = read_file(filename2)

    result = pattern_match(txt, pat)

    # Learned how to open a text file and write into it from 
    # https://www.w3schools.com/python/python_file_write.asp
    with open("output_a2q2.txt", 'w') as f:
        for index in range(len(result)):
            f.write(str(result[index]+1) + '\n')

