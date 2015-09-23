# Cryptobank

A cryptosystem for checks
Inscription du client a la banque
S'assurer que le client a bien un compte avec la banque. Il faut en effet que chaque marchant puissent s'assurer que les chèques ne sont pas des faux.
En plus, il faut que la banque soit sûre de ne pas recevoir des chèques valides qui n'appartiennent à aucun client.
Le client génère une paire de clef RSA.
La banque génère une paire de clef RSA.
La banque signe avec sa clef privée la clef publique du client et envoie cette signature au client (CS).
Inscription d'un marchant à la banque
Il faut que chaque marchant puisse s'assurer que la signature du client est valide.
Le marchant récupère la clef publique de la banque et la stocke
Création d'un article
Il y a plusieurs choses à vérifier : 
1. Que le client ne puisse utiliser le même chèque pour plusieurs transaction
2. Que le marchant ne puisse générer tout plein de chèque valide au nom du client
Vérification par le marchant que le client est bien un client de la banque
Le client envoie la signature ainsi que sa clef publique au marchant.
Le marchant vérifie grâce a la clef publique de la banque que la signature du client est valide
Le marchant envoie au client un message chiffré
Le client le déchiffre et l'envoie au marchant
Si le message est le bon, le marchant envoie un nombre aléatoire (ou un numéro de transaction qu'il incrémente a chaque transaction) au client + id du client + destinataire.
Le client signe avec sa clef privée le message suivant : montant de la transaction, identifiant du commerçant, numéro aléatoire envoyé par le marchant.
Le marchant vérifie que cette signature est valide grâce à la clef publique du client
Si la signature est valide, la transaction est validée.
La banque doit garder le token
A FAIRE
Description du cheque
4 programmes
commercant produit une facture
client fabrique le cheque
le commervant verifie le cheque
banque encaisse ou pas
ex : taper commercar_facture une somme genere une facture
on donne ca en entrée d'un autre prog qui génère le 
pouvoir passer les fichiers d'entrée en param
