#!/bin/bash

function createKeys {
    openssl genrsa -out $1.key 1024
    openssl rsa -in $1.key -pubout -out $1.pubkey


}

function random {
    head -c 16 /dev/urandom | base64
}

function createTransaction {
# montant
# id marchant
# token
# clef publique customer
    echo -n "$1
$2
`random`
`cat $3`"

}

function getNthLineFile {
    sed -n $1p < $2
}


function signTransaction {
    # <transaction to verify> <name of signed transaction>
    montant=`getNthLineFile 1 $1`
    id_marchant=`getNthLineFile 2 $1`
    token=`getNthLineFile 3 $1`
    
    signature="$montant#$id_marchant#$token"
    
}


function signTransaction {
    # <transaction to sign> <name of signed transaction>
    montant=`getNthLineFile 1 $1`
    id_marchant=`getNthLineFile 2 $1`
    token=`getNthLineFile 3 $1`
    signature="$montant#$id_marchant#$token"
    touch $2
    head -3 $1 > $2
    mkdir tmp
    echo $signature > tmp/sign.tmp
    echo "" >> $2
    ./sign.sh tmp/sign.tmp customer.key >> $2
    rm tmp -rf
}

echo "creation des clefs de la banque"
createKeys "bank"
echo "creation des clefs du client"
createKeys "customer"

echo "signing the customer's key"
./sign.sh customer.pubkey bank.key > customer.pubkey.signed

createTransaction 40 1 customer.pubkey.signed > transaction.txt

signTransaction transaction.txt cheque.txt



