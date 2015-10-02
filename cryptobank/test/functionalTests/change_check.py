import unittest
from cryptobank.merchant import verify_transaction
from cryptobank.bank import verify_signature_check
from cryptobank.monrsa.tools import import_key, unserialize, serialize
from cryptobank.monrsa.crypto import Key




class TestCrypto(unittest.TestCase):
    """
    Test a change in the check from the customer
    Test a change in the check from the merchant
    """
    

    
    def test_customer_change_check(self):
        path = "./cryptobank/test/functionalTests/keys/"
        arguments1 = [path + "transaction.json", path + "check.json", path + "customer.pubkey"]
        arguments2 = [path + "transaction2.json", path + "check2.json", path + "customer.pubkey"]
        arguments3 = [path + "transaction2.json", path + "check.json", path + "customer.pubkey"]
        arguments4 = [path + "transaction.json", path + "check2.json", path + "customer.pubkey"]
        """
        Test that a signed check is correctly recognised by the merchant 
        """
       
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
        
    def test_merchant_changed_check(self):
        path = "./cryptobank/test/functionalTests/keys/"
        """
        Check that a merchant cannot change the content of a check without the bank noticing
        """
        client_key = Key.import_key_from_path(path + "customer.pubkey")
        with open(path + "check.json", "r") as file_:
            signed_check = unserialize(file_.readline())
        
        check_signature = signed_check["signature"]
        base64_check = signed_check["base64_check"]
         
        self.assertTrue(verify_signature_check(client_key, check_signature, base64_check))
         
        #
        false_check = unserialize(base64_check)
        false_check["amount"] = 100 
        false_check_64 = serialize(false_check).decode()
        self.assertFalse(verify_signature_check(client_key, check_signature, false_check_64))
