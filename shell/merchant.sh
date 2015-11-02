#!/bin/bash
. transaction.sh

function usage {
    echo "-a [montant][id bank][customer signed key]: creation d'un cheque"
    echo "-b [cheque][customer pub key][bank pub key][transaction]: verif clef"
    echo "-c [transation][cheque]: verification du cheque"


}
if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “abc” OPTION 
    do 
        case $OPTION in 
            a) 
                createTransaction $2 $3 $4 
                ;; 

            b)
                verifyCustomerPubKey $2 $3 $4 
                if [ $? -eq 0 ]
                then
                    echo "[marchant] Le marchant vérifie que cette signature est valide grâce à la clef publique du client"
                    verifyChequeSignature $2 $5 $3
                    if [ $? -eq 0 ]
                    then
                        echo "[marchant] OK" 
                    else
                        echo "soucis"
                    fi
                else
                    echo "There was a problem with this check"
                fi
                ;;
            c)
                echo "[marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)"
                verifyChequeContent $2 $3
                ;;
            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

