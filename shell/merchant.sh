#!/bin/bash
. transaction.sh

if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “Ahpvozacn” OPTION 
    do 
        case $OPTION in 
            a) 
                echo "[marchant] Le marchant crée un chèque avec"
                createTransaction 40 1 customer.pubkey.signed > transaction.txt
                ;; 

            b)
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
                ;;
            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

