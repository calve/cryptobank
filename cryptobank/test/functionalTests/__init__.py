from cryptobank.monrsa.crypto import Key, generate_keys
from cryptobank.customer import sign_check, forge_check
from cryptobank.bank import sign_key
from cryptobank.merchant import new_transaction
from cryptobank.monrsa.tools import import_key, unserialize



path = "./cryptobank/test/functionalTests/keys/"
customerKey = generate_keys()
bankKey = generate_keys()
bankKeyFalse = generate_keys()
# creation de tout ce qu'il faut pour signer des cheques et les verifier
with open(path + "bankFalse.key", "w") as file_:
    file_.write(str(bankKey.get_private().decode()))
with open(path + "bank.key", "w") as file_:
    file_.write(str(bankKey.get_private().decode()))
with open(path + "bank.db", "w") as file_:
    file_.write("")
with open(path + "customer.pubkey", "w") as file_:
    file_.write(str(customerKey.get_pub().decode()))
with open(path + "customer.key", "w") as file_:
    file_.write(str(customerKey.get_private().decode()))
with open(path + "customer.signedkey", "w") as file_:
    file_.write(str(customerKey.get_pub().decode()))
signature = sign_key(path + "customer.pubkey", path + "bank.key")
signature_false = sign_key(path + "customer.pubkey", path + "bankFalse.key")
#creation de 2 cheques valide
print("creation cheque")
with open(path + "transaction.json", "w") as file_:
    file_.write(new_transaction(path + "customer.signedkey", str(100)))
with open(path + "transaction2.json", "w") as file_:
    file_.write(new_transaction(path + "customer.signedkey", str(520)))
with open(path + "check.json", "w") as file_:
    file_.write(sign_check(path + "transaction.json", path + "customer.key"))
with open(path + "check2.json", "w") as file_:
    file_.write(sign_check(path + "transaction2.json", path + "customer.key"))

# creation d'un check qui a le meme token
# import d'un check et recuperation de son token
with open(path + "transaction.json", "r") as file_:
    check_to_forge = unserialize(file_.readline().encode())
arguments = [path + "transaction.json", check_to_forge["token"]]

with open(path + "checkSameToken.json", "w") as file_:
    file_.write(forge_check(arguments, path + "customer.key"))


#creation d'un cheque qui ne devrait pas etre valide car signe par un client d'une autre banque
with open(path + "customerFalse.pubkey", "w") as file_:
    file_.write(str(customerKey.get_pub().decode()))
with open(path + "customerFalse.signedkey", "w") as file_:
    file_.write(str(customerKey.get_pub().decode()))
