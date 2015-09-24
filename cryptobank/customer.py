from monrsa import Key

def sign_check(privatekeypath, transactionpath):
    privatekey = Key.import_key(privatekey_string)
    signature = privatekey.sign(transaction_string)
    return signature
