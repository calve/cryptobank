#! /usr/bin/env python3
"""
A program emuling a cryptographic bank.
"""
import sys
import argparse

from cryptobank.monrsa.crypto import Key
from cryptobank.monrsa.tools import save_rsa_keys, generate_database, unserialize, create_data_to_sign


def verify(check, pubkey):
    custommer_key = RSA.importKey(pubkey)
    custommer_key.verify(check['signature'])





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


#def check_customer_exists(pubkey, signature)
    """
    We want to make sure two things :
        - Check that the signature used to do the transaction is valid
        - 
    """

def store_check(check, bank_db="bank.db"):
    with open(bank_db, "a") as file_:
        file_.write(check)


def verify_signature_check(customer_pub_key, signature, raw_data):
    """
    Verify that a check has not been altered by the merchant
    """
    #return True 
    if customer_pub_key.verify(raw_data, signature):
        return True
    else:
        print("This check has been altered and cannot be accepted")
        return False



def verify_check_first(dic_check, bank_db="bank.db"):
    """
    Checks that the check has not been altered
    """
    with open(bank_db, "r") as file_:
        f = file_.readline()
        while f:
            f_u = unserialize(f)
            if f_u == dic_check:
                print("This check has already been cashed in.")
                exit(1)
            if f_u["token"] == dic_check["token"] and f_u["merchant_id"] == dic_check["merchant_id"]:
                print("the token has already been used... something fishy is going on, we cannot accept this check")
                exit(1)
            f = file_.readline()
        # if we cannot find the same check
        return True
    

def deposit(arguments):
    """
    Verify that the check has been signed by an authorised person
    Verify that the content of the check has not been altered
    Verify that the check has not been already cashed
    Store the check in the db
    """
    with open(arguments[0], "r") as file_:
        signed_check = unserialize(file_.readline())
    
    client_key = Key.import_key_from_path(arguments[1])    
    bank_key = Key.import_key_from_path(arguments[2])
    # the signature of the check
    check_signature = signed_check["signature"]
    # the check encoded in base64
    base64_check = signed_check["base64_check"]
    # the check as a string
    dic_check = unserialize(base64_check)
    # the customer's signature (the one used to sign the check)
    customer_signature = dic_check["signature_customer_public_key"]
    data_signed_by_customer = create_data_to_sign(base64_check) 
    #if the customer is part of the bank, the signature present in the check should be OK
    # check that the check has not already been cashed-in/altered in some way
    if verify_signature_check(client_key, check_signature, data_signed_by_customer):

        if verify_check_first(dic_check):
            print("This check has been cashed in")
            store_check(base64_check)
            exit(0)
        else:
            print("This check has already been cashed-in")
            exit(1)
    else:
        print("This check has been altered and connot be cashed in")
        exit(1)

def main():
    # Install the argument parser. Initiate the description with the docstring
    argparser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    argparser.add_argument("--generate-database",  # This is a binary option
                           action="store_true",
                           help="Generate the databases")
    argparser.add_argument("--generate-keys",  # This is also a binary option
                           action="store_true",
                           help="Generate the keys")
    argparser.add_argument("--sign-key",  # this is a option which need one extra argument
                           help="sign the specified key")
    argparser.add_argument("--deposit",  # this is a option which need one extra argument
                            nargs=3,
                            metavar=("SIGNED_CHECK.JSON", "CUSTOMER.PUBKEY", "BANK.KEY"),
                           help="deposit a check")
    arguments = argparser.parse_args()

    # Now do things depending of the collected arguments
    if arguments.generate_database:
        generate_database("bank.db")
    if arguments.generate_keys:
        save_rsa_keys("bank.pubkey", "bank.key")
    if arguments.sign_key:
        print(sign_key(arguments.sign_key).decode())
    if arguments.deposit:
        deposit(arguments.deposit)

# This is a Python's special:
# The only way to tell wether we are running the program as a binary,
# or if it was imported as a module is to check the content of
# __name__.
# If it is `__main__`, then we are running the program
# standalone, and we run the main() function.
if __name__ == "__main__":
    main()
