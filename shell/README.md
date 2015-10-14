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

