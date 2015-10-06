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
        arguments1 = [path + "transaction.json", path + "check.json", path + "customer.pubkey", path + "customer.signedkey"]
        arguments2 = [path + "transaction2.json", path + "check2.json", path + "customer.pubkey", path + "customer.signedkey"]
        arguments3 = [path + "transaction2.json", path + "check.json", path + "customer.pubkey", path + "customer.signedkey"]
        arguments4 = [path + "transaction.json", path + "check2.json", path + "customer.pubkey", path + "customer.signedkey"]
        """
        Test that a signed check is correctly recognised by the merchant 
        """
       
        """ 
        we check that the check 1 correctly recognised with trasaction 1 
        """
        with open(path + "bank.db", "w") as file_:
            file_.write("")
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments1, path + "bank.pubkey", path + "customer.pubkey")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)
        
        """ 
        we check that the check 2 correctly recognised with trasaction 2 
        """
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments2, path + "bank.pubkey", path + "customer.pubkey")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 0)

        
        """ 
        we check that the check 1 is NOT recognised with trasaction 2 
        """
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments3, path + "bank.pubkey", path + "customer.pubkey")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
        
        """ 
        we check that the check 2 is NOT recognised with trasaction 1 
        """
        with self.assertRaises(SystemExit) as cm:
            verify_transaction(arguments4, path + "bank.pubkey", path + "customer.pubkey")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
        
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
         
        # check that if someone has changed something to the check, the bank does not accept the check
        false_check = unserialize(base64_check)
        false_check["amount"] = 100 
        false_check_64 = serialize(false_check).decode()
        self.assertFalse(verify_signature_check(client_key, check_signature, false_check_64))
