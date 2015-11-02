#!/bin/bash
. transaction.sh

function usage {
    echo "-a: creation de la clef de la banke"
    echo "-b [cheque.txt][customer.pubkey][bank.pubkey]: verification de la signature du client"
    echo "-c [bank.db][cheque.txt]: encaissement du cheque"


}

if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “abc” OPTION 
    do 
        case $OPTION in 
            a) 
                echo "creation des clefs de la banque"
                createKeys "bank"
                ;; 
            b)
                echo -n "[bank] La banque vérifie la signature du client"
                verifyCustomerPubKey $2 $3 $4
                if [ $? -eq 0 ]
                then
                    echo "... OK"
                else
                    echo "... NOK"
                fi
                ;;
            c)
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

