#! /usr/bin/env python3
from monrsa.crypto import Key, generate_keys
from monrsa.tools import save_rsa_keys, import_key, serialize
import argparse
import sys
import random
import json

def print_error(string):
    print(string)
    return False


def check_key(signed_key):

    """
    Will check that the key passed as a parameter is correct
        - loads the bank's public key
        - opens the signature
        - opens the client's public key
        - checks the key again the signature
    """
    '''
    bank_key  = Key.import_key_from_path("bank.pubkey")
    signature = import_key(signed_key)
    with open("customer.pubkey", "r") as file_:
       customer_key = file_.read()
    print(bank_key.verify(customer_key, signature))
    '''

def save_transaction_to_database(transaction):
    """
    Saves the transaction to the bank's database

    """
    with open("bank.db", "a") as file_:
        file_.write(json.dumps(transaction) + "\n")

def create_check(signature, amount):
    """
    Creates a check to sign
    """
    random_number = random.getrandbits(128)
    check = {
        "amount": amount,
        "signature_customer_public_key": signature,
        "merchant_id": "01",
        "token": random_number
    }
    save_transaction_to_database(check)
    print(serialize(check).decode())

def new_transaction(signed_key, amount):
    """
    Generates a new transaction.
    Checks that the customer's key is valid
    iGenerates a check for the customer to sign
    
    """
    
    # we import the signature
    with open(signed_key, "r") as file_:
        signature = file_.readline().strip()
    #check_key(signed_key)
    create_check(signature, amount)
    
    '''    with open(bankfile) as file_:
        bankkey = Key.import_key(file_.readlines())
    if not bankkey.verify(signedkey):
        print("nope, not a client")
        return
    json = {
        "amount" : amount
    }
    return json
'''

def check_transaction(transaction):
    """
    Import le check et le transform en string
    Transform le check de base64 en string
    Verifie que les informations dans le cheque sont les même qu'il a envoyé
    Si OK
        Verifie que la signature est valide
        Si OK : renvoie 0 sur la sortie standard
        Sinon : renvoie 1
    """
    

def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    argparser.add_argument("--new-transaction",  # This is a binary option
                           help="Checks that the customer's key is correct and if so, creates a check ready to be signed")
    argparser.add_argument("--verify-transaction",  # This is also a binary option
                            nargs=3,
                            metavar=('TRANSACTION.JSON', 'SIGNED_CHECK.JSON', 'CLIENT_PUB_KEY.PUBKEY'),
                            help="Checks that the check is valid. If it is OK it returns 0, otherwise it returns 1")
    argparser.add_argument("--amount",  # This is also a binary option
                           help="The amount of the transaction")
    argparser.add_argument("--generate-database",  # This is also a binary option
                           action="store_true",
                           help="Checks that the check is valid. If it is OK it returns 0, otherwise it returns 1")
    arguments = argparser.parse_args()

    # Now do things depending of the collected arguments
    if arguments.new_transaction:
        if arguments.amount:
            new_transaction(arguments.new_transaction, arguments.amount)   
        else:
            print("ko")
    if arguments.transaction:
       check_transaction(arguments.transaction) 


# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()

