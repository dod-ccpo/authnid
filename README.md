# authnid

[![Build Status](https://travis-ci.org/dod-ccpo/authnid.svg?branch=master)](https://travis-ci.org/dod-ccpo/authnid)

## Back end local development

To build, run `script/sertup`.  `script/server` starts the stack with Docker Compose:

* DNS will handle redirecting `dev.cac.atat.codes` to localhost. So, in your browser, go to: http://dev.cac.atat.codes.

The `docker-compose.override.yml` file for local development has a host volume with your app files inside the container for rapid iteration. So you can update your code and it will be the same code (updated) inside the container. You have to restart the server, but you don't need to rebuild the image to test a change. Make sure you use this only for local development. Your final production images should be built with the latest version of your code and do not depend on host volumes mounted.

### Back end tests

To test the back end run:

```bash
script/test
```

The tests run with Pytest. Modify and add tests to `./tests/`.

### SSL Certificates for Testing

The `ssl` directory contains example certs for configuring the regular server SSL, client authentication, and the client certificates currently written to the sample PIVKey. It also contains a script, `make-certs.sh`, which can be used to write a new certificate authority and sign a CSR for the server SSL. The script writes the CSR to list multiple valid hosts (`subjectAltName`) so that the final cert can work across environments (like docker, for instance, where it's host name is "backend").

note: add info about the intermediate CAs

### Intermediate CAs

We are using `pyopenssl` for CRL checks. Currently, this requires that the intermediate CAs for any client CAs be in the CA chain. If you have a DDS CAC card and want to test for local development, you need to add the right intermediate CA before spinning up the server. To do this:

- Try a different CAC-enabled site and pay attention the CA listed next to the cert you use in the browser certificate prompt (for instance, if you log in with an email cert and it says "CA-43" next to your cert, you need "DOD EMAIL CA-43.cer").
- Download the corresponding intermediate cert here: https://militarycac.com/maccerts/
- Convert the cert from DER to PEM format:

```
openssl crl -inform DER -outform PEM -in [path to the downloaded cert] -out cert-output.pem
```

- Then you need to append it to the CA bundle:

```
cat cert-output.pem >> ssl/server-certs/ca-chain.pem
```

- Build and start the server as outlined above. Now your intermediate cert is part of the CA chain that both NGINX and the CRL validator use.
