import unittest
from cryptobank.bank import verify_check_first, store_check
from cryptobank.monrsa.tools import import_key, unserialize, serialize
from cryptobank.monrsa.crypto import Key




class TestCrypto(unittest.TestCase):
    """
    Test a change in the check from the customer
    Test a change in the check from the merchant
    """
    

    
    def test_modif_cheque(self):
        path = "./cryptobank/test/functionalTests/keys/"
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
        


