import unittest
import string
import random
import cryptobank.merchant
from cryptobank.monrsa.crypto import Key
from cryptobank.monrsa.tools import import_key





class TestCrypto(unittest.TestCase):



    def test_sign_small_string(self):
        """
        Test that we only accept a client with a signature from the bank
        """
        bankKey = Key.import_key_from_path("bank.key")
        
        signature = import_key("customer.signedkey")
        with open("customer.pubkey", "r") as file_:
            customer_key = file_.read()
        self.assertTrue(bankKey.verify(customer_key, signature))

