
import unittest
import string
import random
from merchant import *


class TestCrypto(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        """
        Runned once
        """
        self.keys = generate_keys()



    def test_check_client_ok(self):
        """
        Test that we can sign and verify a small string
        """
        key = self.keys
        for i in range(1, 11):
            random_word = randomword(2 ** i)
            signature = key.sign(random_word)
            try:
                self.assertTrue(key.verify(random_word, signature))
            except AssertionError:
                print("Failed to sign string of length {}".format(2 ** i))
                raise

