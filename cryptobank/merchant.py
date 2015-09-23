from monrsa import Key

def new_transaction(amount, signedkey):
    with open(bankfile) as file_:
        bankkey = Key.import_key(file_.readlines())
    if not bankkey.verify(signedkey):
        print("nope, not a client")
        return
    json = {
        "amount" : amount
    }
    return json

def verify_transaction(transactionpath, checkpath, clientpubkeypath):
    clientpubkey = Key.import_key(clientpubkeypath)
    # verify check['transaction']==transaction
    signature = check['signature']
    clientpubkey.verify(rawdata, signature)
