import random

def get_prime(n):
    """Return a prime inferior to n"""
    return n-1

def get_e(phi):
    return 1

def invmod(a, b):
    return 1

def generate_keys(n=2048):
    p = get_prime(n)
    q = get_prime(n)
    n = p * q
    phi = n - (p + q - 1)
    e = get_e(phi)
    d = invmod(e, phi)
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
    
    def sign(self, rawdata):
        return ""

    def verify(self,):
        return False
