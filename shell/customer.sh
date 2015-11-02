#!/bin/bash
. transaction.sh


function usage {
    echo "-a: creation de la clef du client"
    echo "-b [customer.pubkey][bank.key]: signature de la clef du client"
    echo "-c [transaction][cheque]: signature de la transaction"


}

if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “abc” OPTION 
    do 
        case $OPTION in 
            a) 
                #echo "creation des clefs du client"
                createKeys "customer"
                ;; 
            b)   
                #echo "signing the customer's key"
                ./sign.sh $2 $3 
                ;;
            c)
                #echo "[client] Le client signe avec sa clef privée le message contenant"
                signTransaction $2 $3
                ;;
            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

