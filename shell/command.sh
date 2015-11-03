#!/bin/bash
function cleanDir {
    rm *key
    rm *db
    rm *txt
    rm *signed
}


function normalTest {
    cleanDir
    
    echo "[bank] creation des clefs du client"
    ./bank.sh -a

    echo "[customer] creation des clefs du client"
    ./customer.sh -a

    echo "[bank] signing the customer's key"
    ./bank.sh -b customer.pubkey bank.key customer.pubkey.signed

    echo "[marchant] Le marchant crée un chèque avec"
    ./merchant.sh -a 40 1 customer.pubkey.signed > transaction.txt

    echo "[client] Le client signe avec sa clef privée le message contenant"
    ./customer.sh -c transaction.txt cheque.txt

    echo "[marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide"
    ./merchant.sh -b cheque.txt customer.pubkey bank.pubkey transaction.txt

    echo "[marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)"
    ./merchant.sh -c transaction.txt cheque.txt

    echo -n "[bank] La banque vérifie la signature du client"
    ./bank.sh -c cheque.txt customer.pubkey bank.pubkey

    echo -n "[bank] La banque vérifie le token du marchand"
    ./bank.sh -d bank.db cheque.txt
}

function usage {
    echo "-a: normal transaction"
    echo "-R: clean dir"
}

if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “aR” OPTION 
    do 
        case $OPTION in 
            a) 
                echo "creation des clefs de la banque"
                normalTest
                ;; 
            R) 
                echo "Cleaning dir"
                cleanDir
                ;; 
            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

