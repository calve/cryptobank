import unittest
import string
import random
import cryptobank.merchant
from cryptobank.bank import sign_key
from cryptobank.monrsa.crypto import Key, generate_keys
from cryptobank.monrsa.tools import import_key





class TestCrypto(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """
        Runned once
        """
        self.path = "./cryptobank/test/functionalTests/keys/"
        self.customerKey = generate_keys()
        self.bankKey = generate_keys()
        self.bankKeyFalse = generate_keys()
        with open(path + "bank.key", "w") as file_:
            file_.write(str(self.bankKey.get_private().decode()))
        with open(path + "bank.db", "w") as file_:
            file_.write("")
        with open(path + "bankFalse.key", "w") as file_:
            file_.write(str(self.bankKey.get_private().decode()))
        with open(path + "customer.pubkey", "w") as file_:
            file_.write(str(self.customerKey.get_pub().decode()))
        
        self.signature = sign_key(path + "customer.pubkey", path + "bank.key")
        self.signature_false = sign_key(path + "customer.pubkey", path + "bankFalse.key")




    def test_client_auth(self):
        """
        Test that we only accept a client with a signature from the bank
        """
        customer_key = self.customerKey.get_pub().decode()
        

        self.assertTrue(self.bankKey.verify(customer_key, self.signature))
        self.assertFalse(self.bankKey.verify(customer_key, self.signature_false))
        # TO DO : je ne comprend pas pourquoi on a un retour true ici
        self.assertFalse(self.bankKeyFalse.verify(customer_key, self.signature))




    
    def test_modif_cheque(self):
        """
        Test a change in the check from the customer
        Test a change in the check from the merchant
        """
    
        path = self.path
        #empty the db
        open(path + "bank.db", 'w').close()
        with open(path + "check.json", "r") as file_:
            signed_check = unserialize(file_.readline())
        
        base64_check = signed_check["base64_check"]
        dic_check = unserialize(base64_check)
                                           
        self.assertTrue(verify_check_first(dic_check, path+"bank.db"))
        # sauvegarde du check dans la db
        store_check(base64_check, path + "bank.db")
        
        #verification que il ne peut être re-encaisse
        with self.assertRaises(SystemExit) as cm:
            verify_check_first(dic_check, path+"bank.db")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)

        # verif utilisation du meme token pour deux cheque avec differents token
        with open(path + "checkSameToken.json", "r") as file_:
            signed_check_same_token = unserialize(file_.read())
        base64_check = signed_check_same_token["base64_check"]
        dic_check = unserialize(base64_check)
        #verification que il ne peut être re-encaisse
        with self.assertRaises(SystemExit) as cm:
            verify_check_first(dic_check, path+"bank.db")
        the_exception = cm.exception
        self.assertEqual(the_exception.code, 1)
