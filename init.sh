## Initialisation

echo "Generate bank database and keys"
./bank --generate-database
./bank --generate-keys  # crée bank.pubkey & bank.key


echo "Generate merchant database"
./merchant --generate-database


echo "Generate customer key"
./customer --generate-keys # crée customer.pubkey & customer.key

echo "Sign customer key by the bank"
./bank --sign-key customer.pubkey > customer.signedkey

echo "Le marchant prépare le chèque pour le client"
#  - il vérifie la clé signé du client
#  - si ok, il crée un json pret-a-signer
./merchant --new-transaction customer.signedkey --amount 42 > transaction.json

echo "Le client importe sa signature privé, prend le chèque(transaction.json), et appose sa signature"
./customer --private-key customer.key transaction.json > check.json

echo "Le marchant vérifie que le chèque est conforme à la transaction"
# Écris sur la sortie standard `ok` ou `pas ok`
# Retourne 0 si OK, 1 si KO
./merchant --transaction transaction.json --check check.json --client-pubkey client.pubkey

## if last_return_code == ok
##

echo "La banque vérifie que le chèque est valide et l'encaisse"
./bank --deposit check.json
