import unittest
from cryptobank.monrsa.crypto import generate_keys, Key

class TestCrypto(unittest.TestCase):

    def test_signature(self):
        key = generate_keys()
        random_words = "unephraseauhasard"
        signature = key.sign(random_words)
        self.assertTrue(key.verify(random_words, signature))
        self.assertFalse(key.verify("plopplopplop", signature))
        self.assertFalse(key.verify(random_words, "notasignature"))
