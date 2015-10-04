#! /usr/bin/env python3
from cryptobank.monrsa.crypto import Key
from cryptobank.monrsa.tools import save_rsa_keys, serialize, unserialize, create_data_to_sign
import sys
import argparse
import json


def import_check(path):
    """
    Import the check to sign
    """
    
    with open(path, "r") as file_:
        check_str = file_.readline()
    return check_str 
    


def sign_check(arguments, customer_key="customer.key"):
    """
    Import the check to sign
    Import the customer's private key
    Sign the check
    Create a new check that contains : 
        - the base64 version of the check
        - the signature of the base64
    Prints a base64 signed check
    """
    check = import_check(arguments)
    privatekey = Key.import_key_from_path(customer_key)
    
    data_to_sign = create_data_to_sign(check)
    signature = privatekey.sign(data_to_sign).decode()
     
    signed_check = {
        "base64_check": check,
        "signature": signature
    }
    return serialize(signed_check).decode()


def forge_check(arguments):
    check = import_check(arguments[0])
    privatekey = Key.import_key_from_path("customer.key")
    dic_check = unserialize(check)
    dic_check["token"] = arguments[1]
    check = serialize(dic_check).decode()
    privatekey = Key.import_key_from_path("customer.key")
    signature = privatekey.sign(check).decode()
    signed_check = {
        "base64_check": check,
        "signature": signature
    }
    return serialize(signed_check).decode()


def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    argparser.add_argument("--generate-keys",  # This is also a binary option
                           action="store_true",
                           help="Generates the customer's keys")
    argparser.add_argument("--sign-check",  # This is also a binary option
                           metavar=('CHECK-TO-SIGN'),
                           help="Takes a the customer's signature and a check and sign it.")
    argparser.add_argument("--forge-check",  # This is also a binary option
                            nargs=2,
                           metavar=('CHECK-TO-SIGN', "TOKEN"),
                           help="Takes a the customer's signature and a check and sign it.")
    arguments = argparser.parse_args()

    # Now do things depending of the collected arguments
    if arguments.generate_keys:
        save_rsa_keys("customer.pubkey", "customer.key")
    if arguments.sign_check:
        print(sign_check(arguments.sign_check))
    if arguments.forge_check:
        print(forge_check(arguments.forge_check))

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()

