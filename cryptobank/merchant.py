from monrsa.crypto import Key
import sys

def print_error(string):
    print(string)
    return False


def new_transaction(arguments):
    # check that we have an amount in the arguments supplied
    if arguments[3] != "--amount" or len(arguments) != 5:
        print_error("error")
    
    # singnedkey  = Key.import_key_from_path(arguments[2])
    amount      = arguments[4]
      
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
def print_help_message():
    print('help')



# we check that we have more than one argument.
# If not, we print the help message
if len(sys.argv) == 1:
    print_help_message()
else:
    # we check that the transaction to do is a new transaction
    if sys.argv[1] == "--new-transaction":
         new_transaction(sys.argv)   
    # or a transaction (the merchant checks that the signature is valid and that the check's content is the one he expected)
    elif sys.argv[1] == "--transaction":
        print("yoyo")
    else:

        print_help_message()
'''
def verify_transaction(transactionpath, checkpath, clientpubkeypath):
    # verification de la clef du client
    bankpubkey = Key.import_key_from_path(bank.pubkey) 
    clientpubkey = Key.import_key_from(clientpubkeypath)
    # verify check['transaction']==transaction
    signature = check['signature']
    clientpubkey.verify(rawdata, signature)

'''
