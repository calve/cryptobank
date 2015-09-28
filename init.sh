## Initialisation
echo "making a nice and clean new environement"
rm -f *.db *.key *.pubkey *.json

echo "[bank] generating db and keys"
./bank --generate-database
./bank --generate-keys  # crée bank.pubkey & bank.key


echo "[customer] generating customer key"
./customer --generate-keys # crée customer.pubkey & customer.key

echo "[bank] signing the customer's key"
./bank --sign-key customer.pubkey > customer.signedkey

echo "[merchant] preparing the check for the client"
#  - check that the key provided by the customer is accepted by the bank
#  - if it is, it creates a check ready to be signed
./merchant --new-transaction customer.signedkey --amount 42 > transaction.json

echo "[customer] signing the check (importing the private key, taking the check and signing it."
./customer --sign-check transaction.json > check.json

echo "[merchant] checking the check is ok"
# Exit with 0 if OK, 1 if KO
./merchant --verify-transaction transaction.json check.json customer.pubkey 

if [ $? -eq 0 ]
then
    echo "[bank] checking that the check is valid (i.e : that the customer signature is ok and that the check has not already been cashed-in"
    ./bank --deposit check.json customer.pubkey
else
    echo "There was a problem with this check"
fi
