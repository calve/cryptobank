import unittest
import string
import random
import cryptobank.merchant
from cryptobank.monrsa.crypto import Key
from cryptobank.monrsa.tools import import_key



path = "./cryptobank/test/functionalTests/keys/"

class TestCrypto(unittest.TestCase):
    """
    Test a change in the check from the customer
    Test a change in the check from the merchant
    """
    

    def test_customer_change_check(self):
        """
        Test that a bank cannot 
        """
        arguments = ["transaction.json", "check.json", "customer.pubkey"]
        
        bankKey = Key.import_key_from_path(path + "bank.key")
        

        self.assertTrue(bankKey.verify(customer_key, signature))
        self.assertFalse(bankKey.verify(customer_key, signature_false))
        self.assertFalse(bankKeyFalse.verify(customer_key, signature))
        
