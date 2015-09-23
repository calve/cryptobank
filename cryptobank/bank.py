from monrsa import Key, generate_keys

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
