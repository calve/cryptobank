# Shell

## Création du cheque par le commercant

Format du cheque (ligne par ligne) :

    + amount
    + signed_custommer_public_key
    + mechant__id
    + token

## Signature du cheque

    + cheque
    + signature[amount+merchant_id+token]


Pour signer un chèque, on déchiffre, avec la clé privée du client, le
hash du fichier passé en entrée (voir ``sign.sh``).

Pour vérifier un chèque, on chiffre, avec la clé public du client, la
signature passée en entrée. On compare ce résultat au hash du fichier
pour lequel on veut vérifier la signature (voir ``verify.sh``).

## Amélioriations par rapport à la version précédente

Avant, deux marchands pouvaient utiliser le meme token, avec la vulnérabilités suivante :

    + deux marchands complices utilisent le meme token pour deux clients différents
    + les deux chèquent sont signés légitimmement
    + les deux marchands forgent des chèques en échangant les signatures


et donc, deux
marchands possédant des chèques valides, utilisant le meme token,
pouvai

## Tests

Les tests disponibles sont:

### Fonctionnement nominal

Tout les acteurs sont honnêtes, le chèque est signé et encaissé par la
banque.

    [bank] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    .................................++++++
    ........................................++++++
    e is 65537 (0x10001)
    writing RSA key
    [customer] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    ....++++++
    ..................................................................................................................++++++
    e is 65537 (0x10001)
    writing RSA key
    [bank] signing the customer's key
    [marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe
    [client] Le client signe avec sa clef privée le cheque
    [marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide
    [marchant] OK
    [marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)
    [bank] La banque vérifie la signature du client
    [bank] La banque vérifie le token du marchand
    [bank] Check cashed in !
    [bank] OK


### Tentative de fraude : Le client modifie le chèque qu'il signe, le marchand ne l'accepte pas

    [bank] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    .............++++++
    .........++++++
    e is 65537 (0x10001)
    writing RSA key
    [customer] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    .++++++
    .......................................++++++
    e is 65537 (0x10001)
    writing RSA key
    [bank] signing the customer's key
    [marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe
    [marchant] changement du cheque
    [client] Le client signe avec sa clef privée le cheque
    [marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide
    [marchant] OK
    [marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)
    le cheques et la transaction ne sont pas le meme. exit
    [merchant] Le cheque n'est pas le meme
    [marchant] NOK


### Tentative de fraude : Le marchand modifie le chèque à l'insu du client, la banque ne l'accepte pas

    rm: impossible de supprimer « *db »: Aucun fichier ou dossier de ce type
    [bank] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    ..........................++++++
    .......++++++
    e is 65537 (0x10001)
    writing RSA key
    [customer] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    .........++++++
    ......................++++++
    e is 65537 (0x10001)
    writing RSA key
    [bank] signing the customer's key
    [marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe
    [client] Le client signe avec sa clef privée le cheque
    [marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide
    [marchant] OK
    [marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)
    [marchant] Forgerie du cheque
    [bank] La banque vérifie la signature du client
    [bank] La banque vérifie le chèque et le token du marchand
    [bank] Le marchand a changé le cheque
    [bank] NOK


### Tentative de fraude : Le client n'a pas de compte à la banque, le marchand ne l'accepte pas

    =============FAUSSAIRE===============
    [bank fausse] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    ........................................++++++
    ..........................................++++++
    e is 65537 (0x10001)
    writing RSA key
    [customer faux] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    ................................................................................++++++
    .++++++
    e is 65537 (0x10001)
    writing RSA key
    [bank fausse] signing the customer's key
    =============FIN FAUSSAIRE===============
    [bank] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    ....++++++
    ....++++++
    e is 65537 (0x10001)
    writing RSA key
    [marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe
    [client] Le client signe avec sa clef privée le cheque
    [marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide
    [merchant] There was a problem with this check
    [marchant] NOK


### Tentative de fraude : Le marchand essaie d'encaisser plusieurs fois le même chèque, la banque ne l'accepte pas

    [bank] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    ...................................++++++
    ...++++++
    e is 65537 (0x10001)
    writing RSA key
    [customer] creation des clefs du client
    Generating RSA private key, 1024 bit long modulus
    ................++++++
    ..........................................++++++
    e is 65537 (0x10001)
    writing RSA key
    [bank] signing the customer's key
    [marchant] Le marchant crée un chèque avec le montant, son id et sa clef signe
    [client] Le client signe avec sa clef privée le cheque
    [marchant] Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide
    [marchant] OK
    [marchant] Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)
    [bank] La banque vérifie la signature du client
    [bank] La banque vérifie le token du marchand
    [bank] Check cashed in !
    [bank] OK
    TESTING RE-CASHING CHECK
    KkNnkDluM73TqMNOItB6Eg==
    ERROR : token KkNnkDluM73TqMNOItB6Eg== already exists in database
    [bank] NOK
