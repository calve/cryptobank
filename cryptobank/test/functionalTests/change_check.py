import unittest
from cryptobank.merchant import *
from cryptobank.monrsa.tools import import_key




class TestCrypto(unittest.TestCase):
    """
    Test a change in the check from the customer
    Test a change in the check from the merchant
    """
    

    def test_customer_change_check(self):
        """
        Test that a signed check is correctly recognised
        Test that a 
        """
        path = "./cryptobank/test/functionalTests/keys/"
        arguments1 = [path + "transaction.json", path + "check.json", path + "customer.pubkey"]
        arguments2 = [path + "transaction2.json", path + "check2.json", path + "customer.pubkey"]
        arguments3 = [path + "transaction2.json", path + "check.json", path + "customer.pubkey"]
        arguments4 = [path + "transaction.json", path + "check2.json", path + "customer.pubkey"]
       
        """ 
        we check that the check 1 correctly recognised with trasaction 1 
        """
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments1)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)
        
        """ 
        we check that the check 2 correctly recognised with trasaction 2 
        """
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments2)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

        
        """ 
        we check that the check 1 is NOT recognised with trasaction 2 
        """
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments3)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
        
        """ 
        we check that the check 2 is NOT recognised with trasaction 1 
        """
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments4)
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
        #self.assertTrue(bankKey.verify(customer_key, signature))
        #self.assertFalse(bankKey.verify(customer_key, signature_false))
        #self.assertFalse(bankKeyFalse.verify(customer_key, signature))
        
