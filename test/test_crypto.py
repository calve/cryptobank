import unittest
from cryptobank.monrsa.crypto import generate_keys, Key, _is_prime, _get_prime

class TestCrypto(unittest.TestCase):

    def test_signature(self):
        key = generate_keys()
        random_words = "unephraseauhasard"
        signature = key.sign(random_words)
        print(key)
        print(signature)
        self.assertTrue(key.verify(random_words, signature))
        self.assertFalse(key.verify(b"plopplopplop", signature))
        self.assertFalse(key.verify(random_words, b"notasignature"))

    def test_key_gen(self):
        key1 = generate_keys()
        key2 = generate_keys()
        self.assertNotEquals(key1.e, key1.d)
        self.assertNotEquals(key1.e, key2.e)
        self.assertNotEquals(key1.d, key2.d)

    def test_prime(self):
        for n in [1, 3, 5, 7, 13, 17, 31]:
            self.assertTrue(_is_prime(n))
        for n in [4, 6, 9, 15, 20, 100]:
            self.assertFalse(_is_prime(n))

    def test_prime_gen(self):
        self.assertTrue(_is_prime(_get_prime(2048)))
