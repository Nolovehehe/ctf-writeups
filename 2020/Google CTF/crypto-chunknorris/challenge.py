#!/usr/bin/python3 -u

import random
from Crypto.Util.number import *
import gmpy2

a = 0xe64a5f84e2762be5
chunk_size = 64

def gen_prime(bits):
  s = random.getrandbits(chunk_size)
  while True:
    s |= 0xc000000000000001
    print('s', hex(s))
    p = 0
    for _ in range(bits // chunk_size):
      p = (p << chunk_size) + s
      s = a * s % 2**chunk_size
      print(hex(s))
    if gmpy2.is_prime(p):
      return p

p = gen_prime(1024)
print('p', p)
q = gen_prime(1024)
print('q', q)

n = p * q
e = 65537
#flag = open("flag.txt", "rb").read()
flag = b'flag{test}'
print('n =', hex(n))
print('e =', hex(e))
print('c =', hex(pow(bytes_to_long(flag), e, n)))

