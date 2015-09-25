#! /usr/bin/env python3
"""
A program emuling a cryptographic bank.
"""
import sys
import argparse

from monrsa.crypto import Key
from monrsa.tools import save_rsa_keys


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
    return bank_key.sign(data)


def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    argparser.add_argument("--generate-database",  # This is a binary option
                           action="store_true",
                           help="Generate the databases")
    argparser.add_argument("--generate-keys",  # This is also a binary option
                           action="store_true",
                           help="Generate the keys")
    argparser.add_argument("--sign-key",  # This is a option which need one extra argument
                           help="Sign the specified key")
    arguments = argparser.parse_args()

    # Now do things depending of the collected arguments
    if arguments.generate_database:
        generate_database()
    if arguments.generate_keys:
        save_rsa_keys("bank.pubkey", "bank.key")
    if arguments.sign_key:
        print(sign_key(arguments.sign_key).decode())


# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
