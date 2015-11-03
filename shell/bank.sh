#!/bin/bash
. transaction.sh

function usage {
    echo "-a: creation de la clef de la banque"
    echo "-b [customer.pubkey] [bank.key] [output.key]: signature de la clé du client"
    echo "-c [cheque] [customer pub key] [bank pub key]: signature de la clé du client"
    echo "-d [bank.db][cheque.txt]: encaissement du cheque"


}

if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “abcd” OPTION 
    do 
        case $OPTION in 
            a) 
                echo "creation des clefs de la banque"
                createKeys "bank"
                ;; 
            b)
                # usage : -b customer.pubkey bank.key output.signed
                echo -n "[bank] La banque signe la clé du client"
                ./sign.sh $2 $3 > $4
                if [ $? -eq 0 ]
                then
                    echo "... OK"
                else
                    echo "... NOK"
                fi
                ;;
            c)
                echo "[bank] Vérification de la clef du client"
                verifyCustomerPubKey $2 $3 $4
                ;;
            d)
                echo -n "[bank] La banque vérifie le token du marchand"
                touch "bank.db"
                verifyAndRecordToken $2 $3
                if [ $? -eq 0 ]
                then
                    echo "... OK"
                    echo "Check cashed in !"
                else
                    echo "... NOK"
                fi
                ;;
            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

