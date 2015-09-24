## Initialisation

./bank --generate-database
./bank --generate-keys  # crée bank.pubkey & bank.key
./custommer --generate-keys # crée custommer.pubkey & custommer.key
./bank --sign-key custommer.pubkey >> custommer.signedkey

### Transaction


# Le marchant prépare le chèque pour le client
#  - il vérifie la clé signé du client
#  - si ok, il crée un json pret-a-signer
./merchant --new-transaction custommer.signedkey --amount 42 >> transaction.json

# Le client prend le chèque, et appose sa signature
./custommer --private-key custommer.key --sign transaction.json >> check.json

# Le marchant vérifie que le chèque est conforme à la transaction
# Écris sur la sortie standard `ok` ou `pas ok`
# Retourne 0 si OK, 1 si KO
./merchant --transaction transaction.json --check check.json --client-pubkey client.pubkey

## if last_return_code == ok
##

# La banque vérifie que le chèque est valide et l'encaisse
./bank --deposit check.json
