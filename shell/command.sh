echo "creation des clefs du client"
createKeys "customer"

echo "signing the customer's key"
./sign.sh customer.pubkey bank.key > customer.pubkey.signed

echo "[marchant] Le marchant crée un chèque avec"
createTransaction 40 1 customer.pubkey.signed > transaction.txt

echo "[client] Le client signe avec sa clef privée le message contenant"
signTransaction transaction.txt cheque.txt

echo "[marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide"
verifyCustomerPubKey cheque.txt customer.pubkey bank.pubkey

if [ $? -eq 0 ]
then
    echo "[marchant] Le marchant vérifie que cette signature est valide grâce à la clef publique du client"
    verifyChequeSignature cheque.txt transaction.txt customer.pubkey
    if [ $? -eq 0 ]
    then
        echo "[marchant] Le marchant vérifie que cette signature est valide grâce à la clef publique du client"
    else
        echo "soucis"
    fi
else
    echo "There was a problem with this check"
fi

echo "[marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)"
verifyChequeContent transaction.txt cheque.txt

echo -n "[bank] La banque vérifie la signature du client"
verifyCustomerPubKey cheque.txt customer.pubkey bank.pubkey
if [ $? -eq 0 ]
then
    echo "... OK"
else
    echo "... NOK"
fi

echo -n "[bank] La banque vérifie le token du marchand"
touch "bank.db"
verifyAndRecordToken bank.db cheque.txt
if [ $? -eq 0 ]
then
    echo "... OK"
    echo "Check cashed in !"
else
    echo "... NOK"
fi

