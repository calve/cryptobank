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
                echo "creation des clefs du client"
                createKeys "customer"
                ;; 
            b)   
                echo "signing the customer's key"
                ./sign.sh customer.pubkey bank.key > customer.pubkey.signed

            c)
                echo "[client] Le client signe avec sa clef privée le message contenant"
                signTransaction transaction.txt cheque.txt

            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

