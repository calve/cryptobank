#!/bin/bash

tmp=`mktemp -d`


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

function verifyCustomerPubKey {
    # signedCheque.txt customer.pubkey bank.pubkey
    customerPubKey=`getNthLineFile 4 $1`
    echo -n $customerPubKey > $tmp/customKey.tmp
    ./verify.sh $tmp/customKey.tmp $2 $3
}

function verifyChequeSignature {
    # <signe> <original> <<public_key_to_use>
    montant=`getNthLineFile 1 $2`
    id_marchant=`getNthLineFile 2 $2`
    token=`getNthLineFile 3 $2`
    signatureOriginal="$montant#$id_marchant#$token"
    signatureCheque=`getNthLineFile 5 $1`
    echo -n $signatureCheque > $tmp/signatureCheque.tmp
    echo -n $signatureOriginal > $tmp/signatureOriginal.tmp
    echo $tmp/signatureCheque.tmp
    echo $tmp/signatureOriginal.tmp

    ./verify.sh $tmp/signatureCheque.tmp $tmp/signatureOriginal.tmp $3
}

function signTransaction {
    # <transaction to sign> <name of signed transaction>
    montant=`getNthLineFile 1 $1`
    id_marchant=`getNthLineFile 2 $1`
    token=`getNthLineFile 3 $1`
    signature="$montant#$id_marchant#$token"
    touch $2
    cat $1 > $2
    echo -n $signature > $tmp/sign.tmp
    echo "" >> $2
    ./sign.sh $tmp/sign.tmp customer.key >> $2
    rm $tmp/sign.tmp
}


function verifyChequeContent {
    # signedCheck transaction
    for i in `seq 1 4`
    do
    echo $i
    cheque=`getNthLineFile $i $1`
    transaction=`getNthLineFile $i $2`

    if [ "$cheque" != "$transaction" ]
    then
       echo "le cheques et la transaction ne sont pas le meme. exit"
       return 1
    fi
    done
}

function verifyCheckPubkey {
    # Verify that the signed public key contained in the check have been produced by <pub.key>
    # usage : verifyCheckPubkey "check.txt" "pub.key"

    pubkey=`getNthLineFile 4 $1`
    echo -n $pubkey > $tmp/custommer.pubkey.signed
    verifyCustomerPubKey "$tmp/customer.pubkey.signed" $1 $3
}

function verifyAndRecordToken {
    # Usage : verifyAndRecordToken </path/to/database> <cheque.txt>
    # Fails if token is already in database
    token=`getNthLineFile 3 $2`
    database=$1
    grep -wx "$token" $database
    if [ $? -ne 0 ]
    then
        echo $token >> $database
    else
        echo "ERROR : token $token already exists in database"
        return 1
    fi
}


