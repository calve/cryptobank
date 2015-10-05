#! /usr/bin/env python3
from cryptobank.monrsa.crypto import Key, generate_keys
from cryptobank.monrsa.tools import save_rsa_keys, import_key, unserialize, serialize, create_data_to_sign
import argparse
import sys
import random
import json

def print_error(string):
    print(string)
    return False


def check_key(signed_key, bank_pubkey="bank.pubkey", customer_pubkey="customer.pubkey"):

    """
    Will check that the key passed as a parameter is correct
        - loads the bank's public key
        - opens the signature
        - opens the client's public key
        - checks the key again the signature
    """
    bank_key  = Key.import_key_from_path(bank_pubkey)
    signature = import_key(signed_key)
    with open(customer_pubkey, "r") as file_:
       customer_key = file_.read()
    if bank_key.verify(customer_key, signature):
        return True
    else:
        return False


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
    return serialize(check).decode()

def new_transaction(signed_key, amount):
    """
    Generates a new transaction.
    Generates a check for the customer to sign
    
    """
    
    # we import the signature
    with open(signed_key, "r") as file_:
        signature = file_.readline().strip()
    return create_check(signature, amount)



def verify_transaction(arguments, bank_pubkey="bank.pubkey", customer_pubkey="customer.pubkey"):
    """
    Checks that the customer's key is valid
    Import le check et le transform en dic
    Import la transaction d'origine et la transforme en dic
    Verifie que les informations dans le cheque sont les même qu'il a envoyé
    Si OK
        Verifie que la signature est valide
        Si OK : renvoie 0 sur la sortie standard
        Sinon : renvoie 1
    """
    if check_key(arguments[3], bank_pubkey="bank.pubkey", customer_pubkey="customer.pubkey") is False:
        print("The client has not got an account with the bank")
        exit(1)
    
    with open(arguments[0]) as file_:
        original_transaction = unserialize(file_.readline())
    with open(arguments[1]) as file_:
        signed_check = unserialize(file_.readline())
    
    #this is the check that the customer has signed
    signed_transaction = unserialize(signed_check["base64_check"])
    signature = signed_check["signature"]     
    client_key = Key.import_key_from_path(arguments[2]) 
    data_signed_by_customer = create_data_to_sign(signed_check["base64_check"])

# if the two checks match, we just have to check that the signature is ok.
    if signed_transaction == original_transaction:
        if client_key.verify(data_signed_by_customer, signature):
            exit(0)
        else:
            print("The signature does not appear to have been made by the client. Could there be Charly in the middle ? Better being safe than sorry... exiting")
    else:
        print("the check the customer has signed is not the same as the one the merchant signed. Exiting")
        exit(1)

def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    argparser.add_argument("--new-transaction",  # This is a binary option
                           help="Checks that the customer's key is correct and if so, creates a check ready to be signed")
    argparser.add_argument("--verify-transaction",  # This is also a binary option
                            nargs=4,
                            metavar=('TRANSACTION.JSON', 'SIGNED_CHECK.JSON', 'CLIENT_PUB_KEY.PUBKEY', 'CLIENT_SIGNED_KEY.SIGNEDKEY'),
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
            print(new_transaction(arguments.new_transaction, arguments.amount))
        else:
            print("ko")
    if arguments.verify_transaction:
       verify_transaction(arguments.verify_transaction) 


# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()

