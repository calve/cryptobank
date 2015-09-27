#! /usr/bin/env python3
from monrsa.crypto import Key
from monrsa.tools import save_rsa_keys, unserialize
import sys
import argparse
import json


def import_check(path):
    """
    Import the check to sign as a json dictionary
    """
    
    with open(path, "r") as file_:
        check_str = file_.readline()
    return unserialize(check_str))
    

def sign_check(arguments):
    private_key = arguments[0]
    check = import_check(arguments[1]) 
    
    
    #privatekey = Key.import_key(privatekey_string)
    #signature = privatekey.sign(transaction_string)
    #return signature



def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    argparser.add_argument("--generate-keys",  # This is also a binary option
                           action="store_true",
                           help="Generates the customer's keys")
    argparser.add_argument("--private-key",  # This is also a binary option
                           nargs=2,
                           metavar=('PRIVATE-KEY', 'CHECK-TO-SIGN'),
                           help="Takes a the customer's signature and a check and sign it.")
    arguments = argparser.parse_args()

    # Now do things depending of the collected arguments
    if arguments.generate_keys:
        save_rsa_keys("customer.pubkey", "customer.key")
    if arguments.private_key:
        sign_check(arguments.private_key)

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()

