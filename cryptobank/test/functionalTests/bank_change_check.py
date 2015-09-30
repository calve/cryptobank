import unittest
import string
import random
import cryptobank.merchant
from cryptobank.monrsa.crypto import Key
from cryptobank.monrsa.tools import import_key



path = "./cryptobank/test/functionalTests/keys/"

class TestCrypto(unittest.TestCase):

    

    def test_banque_change_check(self):
        """
        Test that a bank cannot 
        """
        bankKey = Key.import_key_from_path(path + "bank.key")
        

        self.assertTrue(bankKey.verify(customer_key, signature))
        self.assertFalse(bankKey.verify(customer_key, signature_false))
        self.assertFalse(bankKeyFalse.verify(customer_key, signature))
        
