import random
from fractions import gcd
import base64
from functools import reduce

def _text2Int(text):
    """Convert a text string into an integer"""
    return reduce(lambda x, y : (x << 8) + y, map(ord, text))

def _int2Text(number, size=512):
    """Convert an integer into a text string"""
    text = "".join([chr((number >> j) & 0xff)
                    for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")

def _get_prime(n):
    """Return a prime inferior to n"""
    while True:
        prime = random.randint(0, n)
        if _is_prime(prime):
            return prime

def _get_e(phi):
    while True:
        e = random.randint(0, phi)
        if gcd(e, phi) == 1:
            return e

def _egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b//a, b % a
        m, n = x-u*q, y-v*q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y

def _invmod(a, m):
    g, x, y = _egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    return 1

def _is_prime(n):
    for x in range(2,n):
        if n%x == 0:
            return False
    return True

def generate_keys(n=2048):
    p = _get_prime(n)
    q = _get_prime(n)
    n = p * q
    phi = n - (p + q - 1)
    e = _get_e(phi)
    d = _invmod(e, phi)
    return Key(n, d, e)

class Key:
    def __init__(self, n, d, e):
        self.n = n
        self.e = e
        self.d = d

    def get_pub():
        return (n, e)

    def get_private():
        return (n, d)

    def import_key(base64_encoded_key):
        return

    def import_key_from_path(filepath):
        """
        Import a key from the specified path
        """
        return

    def sign(self, rawdata):
        raw = _text2Int(rawdata)
        m = raw % self.n
        sign = pow(m, self.d, self.n)
        print("signature : {}".format(sign))
        representable = base64.b64encode(_int2Text(sign).encode())
        return representable

    def verify(self, rawdata, signature):
        binary_sign = base64.b64decode(signature)
        c = _text2Int(binary_sign.decode())
        result = pow(c, self.e, self.n)
        print("verified result {} ({})".format(result, _int2Text(result)))
        return result == _text2Int(rawdata)

    def __str__(self):
        return " - ".join([str(self.n), str(self.e), str(self.d)])
