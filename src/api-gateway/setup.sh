#!/bin/sh

# Ottengo l'indrizzo IP del container
cat /etc/hosts | grep '^172.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' -o > /app/own_ip_address.txt

# Ottengo indirizzo IP container che esegue il servizio di Discovery
dig src-api-gateway-1 | grep '172.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}' -o > /app/server1.txt

# L'indirizzo IP del container in esecuzione
export ARG1=$(cat /app/own_ip_address.txt)

# L'indirizzo IP del primo server di Discovery
export ARG2=$(cat /app/server1.txt)

# Lancio il microservizio
python3 ./discovery.py $ARG1 $ARG2