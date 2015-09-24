from monrsa.crypto import Key
from monrsa.tools import save_rsa_keys 
import sys




def generate_keys():
    keys = generate_keys()
    with open(filename, "w") as file_:
        file_.write(keys.get_pub())
    with open(filename, "w") as file_:
        file_.write(keys.get_private())

def sign(rawdata):
    with open(bankpubkey, "r") as file_:
        bank_privatekey = Key.import_key(file_.readline)
    signature = bank_privatekey.sign(rawdata)
    return signature


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


if len(sys.argv) == 1:
    print_help_message()
else:

    if sys.argv[1] == "--generate-database":
        generate_database()
    elif sys.argv[1] == "--generate-keys": 
        save_rsa_keys("bank.pubkey", "bank.key")

    else:
        print_help_message()
