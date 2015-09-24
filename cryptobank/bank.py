#! /usr/bin/env python3
from monrsa.crypto import Key 
from monrsa.tools import *
import sys
import base64


def verify(check, pubkey):
    custommer_key = RSA.importKey(pubkey)
    custommer_key.verify(check['signature'])



def generate_database():
    """
    Generates a blank file for the bank to use as a database
    """
    db   = open("bank_db.db", "w")
    db.write("")
    db.close()


def sign_key(raw_data_path):
    """
    Sign the key if the customer
    To do so :
        - we import the bank private key
        - we open the customer's public key
        - we sign the public key
        - we print it
    
    """
    bank_key = Key.import_key_from_path("bank.key")
    with open(raw_data_path, "r") as file_:
        data = file_.read()
    data_string = str(unserialize(data))
    return bank_key.sign(data_string)




if len(sys.argv) == 1:
    print_help_message()
else:

    if sys.argv[1] == "--generate-database":
        generate_database()
    elif sys.argv[1] == "--generate-keys": 
        save_rsa_keys("bank.pubkey", "bank.key")
    elif sys.argv[1] == "--sign-key": 
        print(sign_key(sys.argv[2]).decode())

    else:
        print_help_message()
