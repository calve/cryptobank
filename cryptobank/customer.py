from monrsa.crypto import Key
from monrsa.tools import save_rsa_keys 
import sys


def sign_check(privatekeypath, transactionpath):
    privatekey = Key.import_key(privatekey_string)
    signature = privatekey.sign(transaction_string)
    return signature



if len(sys.argv) == 1:
    print_help_message()
else:

    if sys.argv[1] == "--generate-keys": 
        save_rsa_keys("customer.pubkey", "customer.key")

    else:
        print_help_message()
