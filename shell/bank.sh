#!/bin/bash
. transaction.sh



if [ -z "$1" ] 
  then 
    usage 
  else 
    while getopts “Ahpvozacn” OPTION 
    do 
        case $OPTION in 
            c) 
                echo "creation des clefs de la banque"
                createKeys "bank"
                ;; 
            ?) 
                usage 
                exit 
                ;; 
        esac 
    done     
fi 

