import random

def _get_prime(n):
    """Return a prime inferior to n"""
    while True:
        prime = random.randint(0, n)
        if _is_prime(prime):
            return prime

def _get_e(phi):
    return 1

def _invmod(a, b):
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
        return ""

    def verify(self, rawdata, signature):
        return False
