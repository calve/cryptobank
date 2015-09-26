#! /usr/bin/env python3
from monrsa.crypto import Key, generate_keys
from monrsa.tools import save_rsa_keys, import_key
import argparse
import sys


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

def new_transaction(signed_key, amount):
    """
    Generates a new transaction.
    Checks that the customer's key is valid
    iGenerates a check for the customer to sign
    
    """
    check_key(signed_key)
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
def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    argparser.add_argument("--new-transaction",  # This is a binary option
                           help="Checks that the customer's key is correct and if so, creates a check ready to be signed")
    argparser.add_argument("--transaction",  # This is also a binary option
                           action="store_true",
                           help="Checks that the check is valid. If it is OK it returns 0, otherwise it returns 1")
    argparser.add_argument("--amount",  # This is also a binary option
                           help="The amount of the transaction")
    arguments = argparser.parse_args()

    # Now do things depending of the collected arguments
    if arguments.new_transaction:
        if arguments.amount:
            new_transaction(arguments.new_transaction, arguments.amount)   
        else:
            print("ko")
    if arguments.transaction:
        print("yoyo")


# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()

