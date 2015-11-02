#!/bin/bash

./bank.sh -a

# "creation des clefs du client"
./customer.sh -a

# "signing the customer's key"
./bank.sh -b customer.pubkey bank.key customer.pubkey.signed

# "[marchant] Le marchant crée un chèque avec"
./merchant.sh -a 40 1 customer.pubkey.signed > transaction.txt

# "[client] Le client signe avec sa clef privée le message contenant"
./customer.sh -c transaction.txt cheque.txt

# "[marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide"
./merchant.sh -b cheque.txt customer.pubkey bank.pubkey transaction.txt


# "[marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)"
./merchant.sh -c transaction.txt cheque.txt

# -n "[bank] La banque vérifie la signature du client"
./bank.sh -b cheque.txt customer.pubkey bank.pubkey

# -n "[bank] La banque vérifie le token du marchand"
touch "bank.db"
./bank.sh -c bank.db cheque.txt
