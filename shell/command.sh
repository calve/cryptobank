#!/bin/bash
function cleanDir {
    rm *key
    rm *db
    rm *txt
    rm *signed
}


function normalTest {
    cleanDir
    
    echo "[bank] creation des clefs du client" &&
    ./bank.sh -a &&

    echo "[customer] creation des clefs du client" &&
    ./customer.sh -a &&

    echo "[bank] signing the customer's key" &&
    ./bank.sh -b customer.pubkey bank.key customer.pubkey.signed &&

    echo "[marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe" &&
    ./merchant.sh -a 40 1 customer.pubkey.signed > transaction.txt &&

    echo "[client] Le client signe avec sa clef privée le cheque"
    ./customer.sh -c transaction.txt cheque.txt &&

    echo "[marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide"
    ./merchant.sh -b cheque.txt customer.pubkey bank.pubkey transaction.txt &&

    echo "[marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)"
    ./merchant.sh -c transaction.txt cheque.txt &&

    echo -n "[bank] La banque vérifie la signature du client"
    ./bank.sh -c cheque.txt customer.pubkey bank.pubkey &&

    echo -n "[bank] La banque vérifie le token du marchand"
    ./bank.sh -d bank.db cheque.txt customer.pubkey
}

function test1 {
    cleanDir
    # qu'un client ne peut changer le cheque sans que le marchant ne s'en rende compte 
    echo "[bank] creation des clefs du client" &&
    ./bank.sh -a &&

    echo "[customer] creation des clefs du client" &&
    ./customer.sh -a &&

    echo "[bank] signing the customer's key" &&
    ./bank.sh -b customer.pubkey bank.key customer.pubkey.signed &&

    echo "[marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe" &&
    ./merchant.sh -a 40 1 customer.pubkey.signed > transaction.txt &&
    
    echo "[marchant] changement du cheque" &&
    cp transaction.txt transaction2.txt &&
    sed -i -e 's/40/41/g' transaction2.txt &&

    echo "[client] Le client signe avec sa clef privée le cheque" &&
    ./customer.sh -c transaction2.txt cheque.txt &&
    
    echo "[marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide" &&
    ./merchant.sh -b cheque.txt customer.pubkey bank.pubkey transaction2.txt &&

    echo "[marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)" &&
    ./merchant.sh -c transaction.txt cheque.txt &&

    echo -n "[bank] La banque vérifie la signature du client" &&
    ./bank.sh -c cheque.txt customer.pubkey bank.pubkey &&

    echo -n "[bank] La banque vérifie le token du marchand" &&
    ./bank.sh -d bank.db cheque.txt customer.pubkey
}

function test2 {
    #vérification qu'un marchant ne peut changer le cheque sans que la banque ne s'en rendre compte

    cleanDir
    echo "[bank] creation des clefs du client" &&
    ./bank.sh -a &&

    echo "[customer] creation des clefs du client" &&
    ./customer.sh -a &&

    echo "[bank] signing the customer's key" &&
    ./bank.sh -b customer.pubkey bank.key customer.pubkey.signed &&

    echo "[marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe" &&
    ./merchant.sh -a 40 1 customer.pubkey.signed > transaction.txt &&

    echo "[client] Le client signe avec sa clef privée le cheque" &&
    ./customer.sh -c transaction.txt cheque.txt &&

    echo "[marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide" &&
    ./merchant.sh -b cheque.txt customer.pubkey bank.pubkey transaction.txt &&

    echo "[marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)" &&
    ./merchant.sh -c transaction.txt cheque.txt &&

    echo "[marchant] Forgerie du cheque" &&
    sed -i -e 's/40/41/g' cheque.txt &&
    
    echo -n "[bank] La banque vérifie la signature du client" &&
    ./bank.sh -c cheque.txt customer.pubkey bank.pubkey &&

    echo -n "[bank] La banque vérifie le chèque et le token du marchand" &&
    ./bank.sh -d bank.db cheque.txt customer.pubkey

}

function test3 {

    cleanDir
    echo "=============FAUSSAIRE===============" 
    echo "[bank fausse] creation des clefs du client" 
    ./bank.sh -a &&

    echo "[customer faux] creation des clefs du client" &&
    ./customer.sh -a &&

    echo "[bank fausse] signing the customer's key" &&
    ./bank.sh -b customer.pubkey bank.key customer.pubkey.signed &&


    echo "=============FIN FAUSSAIRE===============" 
    echo "[bank] creation des clefs du client"
    ./bank.sh -a &&

    echo "[marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe"
    ./merchant.sh -a 40 1 customer.pubkey.signed > transaction.txt &&

    echo "[client] Le client signe avec sa clef privée le cheque"
    ./customer.sh -c transaction.txt cheque.txt &&

    echo "[marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide"
    ./merchant.sh -b cheque.txt customer.pubkey bank.pubkey transaction.txt


}

function test4 {
    normalTest
    echo "TESTING RE-CASHING CHECK"
    ./bank.sh -d bank.db cheque.txt customer.pubkey
}


function usage {
    echo "-a [normalTest]: normal transaction"
    echo "-b [test1]: vérification que client ne peut changer le cheque sans que le marchant ne s'en rende compte"
    echo "-c [test2]: vérification qu'un marchant ne peut changer le cheque sans que la banque ne s'en rendre compte"
    echo "-d [test3]: vérification qu'un client n'ayant pas une signature de la banque ne puissent pas effectuer d'opérations"
    echo "-e [test4]: vérification que un cheque ne puisse pas être encaissé plusieurs fois"
    echo "-R: clean dir"
}

if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “abcdeR” OPTION 
    do 
        case $OPTION in 
            a) 
                normalTest
                ;; 
            b) 
                test1
                ;; 
            c) 
                test2
                ;; 
            d) 
                test3
                ;; 
            e) 
                test4
                ;; 
            R) 
                cleanDir
                ;; 
            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

