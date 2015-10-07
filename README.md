# Cryptobank

A cryptosystem for checks

## Inscription du client a la banque

S'assurer que le client a bien un compte avec la banque. Il faut en effet que chaque marchant puissent s'assurer que les chèques ne sont pas des faux.
En plus, il faut que la banque soit sûre de ne pas recevoir des chèques valides qui n'appartiennent à aucun client.

 + Le client génère une paire de clef RSA.
 + La banque génère une paire de clef RSA.
 + La banque signe avec sa clef privée la clef publique du client et envoie cette signature au client (CS).

## Inscription d'un marchant à la banque

Il faut que chaque marchant puisse s'assurer que la signature du client est valide.
Le marchant récupère la clef publique de la banque et la stocke

## Création d'un article

Il y a plusieurs choses à vérifier :

  1. Que le client ne puisse utiliser le même chèque pour plusieurs transaction
  2. Que le marchant ne puisse générer tout plein de chèque valide au nom du client

## Vérification par le marchant que le client est bien un client de la banque

  + Le client envoie la signature ainsi que sa clef publique au marchant.
  + Le marchant envoie un nombre aléatoire
  + Le client signe avec sa clef privée le message contenant
    - montant de la transaction ``amount``
    - identifiant du commerçant ``merchant_id``
    - numéro aléatoire envoyé par le marchant ``token``
    - clé publique du client ``signed_custommer_public_key``
  + Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide
  + Le marchant vérifie que cette signature est valide grâce à la clef publique du client
  + Le marchant vérifie que le contenu du chèque est ce qu'il attend (montant, ordre, nombre aléatoire)
  + Si la signature est valide, il remet le chèque à la banque
  + La banque vérifie la signature du client
  + La banque vérifie que le token n'est pas déjà enregistré
  + La banque enregistre le tuple ``(token, id_merchant, id_custommer)``
  + La banque effectue le paiement


## Description du chèque

On représentera et transmettra les chèques en JSON :

### Chèque en clair:

```

{
    "amount": 4200,
    "signed_custommer_public_key": "Y2zDqXB1YmxpcXVlc2lnbsOpCg==",
    "merchant_id": 01,
    "token": "381de8be5e622bcc0bf72d399f907e6b"
}

```


### Chèque signé :

```
signature = #[nb_digit_de_amount]#amounttoken
{
    "transaction": base64,
    "signature":"jajiaji24545gji_uuiyèyaavnvb"
}
```


## Binaires

### Programme client

   - Générer une paire de clé
   - Lire une clé signée
   - Créer un chèque :
      - Entrées :
        - ``token``
        - ``amount``
        - ``merchant_id``
      - Sortie :
        - Chèque signé sur ``stdout``


### Programme marchant

  - Vérifier une signature
  - Générer un ``token``
  - Vérifier le chèque

### Programme banque

  - Générer une paire de clé
  - Signer la clé d'un client
  - Vérifier la signature du chèque
  - Vérifier que le tuple ``(token, merchant, custommer)`` n'est pas déjà dans la base
  - Stockes le tuple ``(token, merchant, custommer)``


### Programme d'initialisation

Crée une paire de clé pour la banque


## Tests

Run units tests with

    python3 -m unittest

from the root directory
Tests :
  + des fonctions principales utilisés par notre bibliothèque rsa
  + qu'un client ne peut changer le cheque sans que le marchant ne s'en rende compte 
  + qu'un marchant ne peut changer le cheque sans que la banque ne s'en rendre compte
  + que un client n'ayant pas une signature de la banque ne puissent pas effectuer d'opérations
  + que un cheque ne puisse pas être encaissé plusieurs fois



## A FAIRE

  + 4 programmes
  + commercant produit une facture
  + client fabrique le cheque
  + le commervant verifie le cheque
  + banque encaisse ou pas
  + ex : taper commercar_facture une somme genere une facture
  + on donne ca en entrée d'un autre prog qui génère le
  + pouvoir passer les fichiers d'entrée en param

## Openssl

### To sign data

    sha1sum <data-to-sign> | openssl rsautl -inkey <private.key> -decrypt -raw | base64 > <data.signed>

### Verify data

    base64 --decode <data.signed> | openssl rsautl -pubin -inkey <public.key> -encrypt -raw
