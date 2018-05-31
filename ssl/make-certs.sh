#!/bin/bash
# Generate the root (GIVE IT A PASSWORD IF YOU'RE NOT AUTOMATING SIGNING!):
echo 'MAKING CA'
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 7300 -key ca.key -sha256 -extensions v3_ca -out ca.crt

# Generate the domain key:
openssl genrsa -out dev.cac.atat.codes.key 2048

echo 'MAKING CSR'
# Generate the certificate signing request
openssl req -nodes -sha256 -new -key dev.cac.atat.codes.key -out dev.cac.atat.codes.csr -reqexts SAN -config <(cat req.cnf <(printf "[SAN]\nsubjectAltName=DNS.1:dev.cac.atat.codes,DNS.2:cac.atat.codes,DNS.3:backend"))

# Sign the request with your root key
openssl x509 -sha256 -req -in dev.cac.atat.codes.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out dev.cac.atat.codes.crt -days 7300  -extfile <(cat req.cnf <(printf "[SAN]\nsubjectAltName=DNS.1:dev.cac.atat.codes,DNS.2:cac.atat.codes,DNS.3:backend")) -extensions SAN

# Check your homework:
openssl verify -CAfile ca.crt dev.cac.atat.codes.crt
