from fractions import gcd
from functools import reduce
from itertools import count, islice
from math import sqrt
import base64
import json
import random
import hashlib
from binascii import Error as binasciiError

_prime_trials = 2


def _text2Int(text):
    """Convert a text string into an integer"""
    return reduce(lambda x, y: (x << 8) + y, map(ord, text))


def _int2Text(number, size=512):
    """Convert an integer into a text string"""
    text = "".join([chr((number >> j) & 0xff)
                    for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")


def _get_prime(n):
    """
    Returns a random prime number of size n bits
    """
    r = 1
    while not _is_prime(r):
        print(".", end="", flush=True)
        r = random.getrandbits(n) | (2**(n-1))
    print("+")
    return r


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


def _is_prime(n):
    """
    Returns whether a number is a prime number
    """
    if n <= 2:
        return False
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)

    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True  # n is definitely composite

    for i in range(_prime_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False

    return True  # no base tested showed n as composite

    if n < 2:
        return False
    return all(n % i for i in islice(count(2), int(sqrt(n)-1)))


def _serialize(o):
    """
    Encode a python dictionnary to a printable base64-encoded string
    """
    return base64.b64encode(json.dumps(o).encode())


def _unserialize(s):
    """
    Decode a base64-encoded string to a python dictionnary
    """
    return json.loads(base64.b64decode(s).decode())


def _hash_function(rawdata):
    return hashlib.sha1(rawdata).hexdigest()


def generate_keys(n=2048):
    p = _get_prime(n//2)
    q = _get_prime(n//2)
    n = p * q
    phi = n - (p + q - 1)
    e = _get_e(phi)
    d = _invmod(e, phi)
    return Key(n, d, e)


class Key:
    def __init__(self, n, e, d=None):
        self.n = n
        self.e = e
        if d:
            self.d = d

    def get_pub(self):
        """
        Returns a base64-encoded string representing the public key
        """
        public_parts = {
            "modulus": self.n,
            "encryption exponent": self.e,
        }
        return _serialize(public_parts)

    def get_private(self):
        """
        Returns a base64-encoded string representing the private key
        """
        private_parts = {
            "modulus": self.n,
            "encryption exponent": self.e,
            "decryption exponent": self.d,
        }
        return _serialize(private_parts)

    @classmethod
    def import_key(cls, base64_encoded_key):
        rawdict = _unserialize(base64_encoded_key)
        k = Key(rawdict["modulus"], rawdict["encryption exponent"])
        if "decryption exponent" in rawdict:
            k.d = rawdict["decryption exponent"]
        return k

    @classmethod
    def import_key_from_path(cls, filepath):
        """
        Import a key from the specified path:
        Usage :
        >>> from monrsa.crypto import Key
        >>> pubkey = Key.import_key_from_path("~/key.pubkey")
        """
        with open(filepath, "r") as file_:
            body = file_.read()
        return cls.import_key(body)

    def sign(self, rawdata):
        # Compute a fixed-length hash, so we don't have to deal with padding
        digest = _hash_function(rawdata.encode())
        raw = _text2Int(digest)
        m = raw % self.n
        sign = pow(m, self.d, self.n)
        representable = base64.b64encode(_int2Text(sign).encode())
        return representable

    def verify(self, rawdata, signature):
        try:
            binary_sign = base64.b64decode(signature)
        except binasciiError:
            return False
        c = _text2Int(binary_sign.decode())
        original = pow(c, self.e, self.n)
        digest = _hash_function(rawdata.encode())
        signed = _int2Text(original)
        # Compare the content of the signed string to the original hash
        return signed == digest

    def __str__(self):
        return self.get_pub().decode()
