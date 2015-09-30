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
        bankKey = Key.import_key_from_path("./cryptobank/test/functionalTests/keys/bank.key")
        bankKeyFalse = Key.import_key_from_path("./cryptobank/test/functionalTests/keys/bankFalse.key")
        signature = import_key("./cryptobank/test/functionalTests/keys/customer.signedkey")
        signature_false = import_key("./cryptobank/test/functionalTests/keys/customerFalse.signedkey")
        with open("./cryptobank/test/functionalTests/keys/customer.pubkey", "r") as file_:
            customer_key = file_.read()
        

        self.assertTrue(bankKey.verify(customer_key, signature))
        self.assertFalse(bankKey.verify(customer_key, signature_false))
        self.assertFalse(bankKeyFalse.verify(customer_key, signature))
        
