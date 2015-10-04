import unittest
import string
import random
from cryptobank.merchant import new_transaction
from cryptobank.customer import sign_check
from cryptobank.bank import sign_key
from cryptobank.monrsa.crypto import Key, generate_keys
from cryptobank.monrsa.tools import import_key, unserialize





class TestCrypto(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """
        Runned once
        """
        self.path = "./cryptobank/test/functionalTests/keys/"
        path = self.path
        self.customerKey = generate_keys()
        self.bankKey = generate_keys()
        self.bankKeyFalse = generate_keys()
        # creation de tout ce qu'il faut pour signer des cheques et les verifier
        with open(path + "bankFalse.key", "w") as file_:
            file_.write(str(self.bankKey.get_private().decode()))
        with open(path + "bank.key", "w") as file_:
            file_.write(str(self.bankKey.get_private().decode()))
        with open(path + "bank.db", "w") as file_:
            file_.write("")
        with open(path + "customer.pubkey", "w") as file_:
            file_.write(str(self.customerKey.get_pub().decode()))
        with open(path + "customer.key", "w") as file_:
            file_.write(str(self.customerKey.get_private().decode()))
        with open(path + "customer.signedkey", "w") as file_:
            file_.write(str(self.customerKey.get_pub().decode()))
        self.signature = sign_key(path + "customer.pubkey", path + "bank.key")
        self.signature_false = sign_key(path + "customer.pubkey", path + "bankFalse.key")
        #creation de 2 cheques valide
        print("creation cheque")
        with open(path + "transaction.json", "w") as file_:
            file_.write(new_transaction(path + "customer.signedkey", str(100)))
        with open(path + "transaction2.json", "w") as file_:
            file_.write(new_transaction(path + "customer.signedkey", str(520)))
        with open(path + "check.json", "w") as file_:
            file_.write(sign_check(path + "transaction.json", path + "customer.key"))
        with open(path + "check2.json", "w") as file_:
            file_.write(sign_check(path + "transaction2.json", path + "customer.key"))

        # creation d'un check qui a le meme token
        # import d'un check et recuperation de son token
        with open(path + "check.json", "w") as file_:
            check_to_forge = unserialize(file_.readline())
        arguments = [path + "check.json", check_to_forge["token"]]
        
        with open(path + "checkSameToken.json", "w") as file_:
            file_.write(forge_check(arguments))
        

        #creation d'un cheque qui ne devrait pas etre valide car signe par un client d'une autre banque
        with open(path + "customerFalse.pubkey", "w") as file_:
            file_.write(str(self.customerKey.get_pub().decode()))
        with open(path + "customerFalse.signedkey", "w") as file_:
            file_.write(str(self.customerKey.get_pub().decode()))
        


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


    def test_client_auth(self):
        """
        Test that we only accept a client with a signature from the bank
        """
        customer_key = self.customerKey.get_pub().decode()
        

        self.assertTrue(self.bankKey.verify(customer_key, self.signature))
        self.assertFalse(self.bankKey.verify(customer_key, self.signature_false))
        # TO DO : je ne comprend pas pourquoi on a un retour true ici
        self.assertFalse(self.bankKeyFalse.verify(customer_key, self.signature))


