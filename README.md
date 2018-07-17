# authnid

[![Build Status](https://travis-ci.org/dod-ccpo/authnid.svg?branch=master)](https://travis-ci.org/dod-ccpo/authnid)

## Installation

### Cloning
This project contains git submodules. Here is an example clone command that will
automatically initialize and update those modules:

    git clone --recurse-submodules git@github.com:dod-ccpo/atst.git

If you have an existing clone that does not yet contain the submodules, you can
set them up with the following command:

    git submodule update --init --recursive

### Back end local development setup

To build, run `script/setup`.  `script/server` starts the stack with Docker Compose:

The `docker-compose.override.yml` file for local development has a host volume with your app files inside the container for rapid iteration. So you can update your code and it will be the same code (updated) inside the container. You have to restart the server, but you don't need to rebuild the image to test a change. Make sure you use this only for local development. Your final production images should be built with the latest version of your code and do not depend on host volumes mounted.

### Back end tests

To test the back end run:

```
./script/test
```

The tests run with Pytest. Modify and add tests to `./tests/`.

### SSL Certificates for Testing

The `ssl` directory contains example certs for configuring the regular server SSL, client authentication, and the client certificates currently written to the sample PIVKey. It also contains a script, `make-certs.sh`, which can be used to write a new certificate authority and sign a CSR for the server SSL. The script writes the CSR to list multiple valid hosts (`subjectAltName`) so that the final cert can work across environments (like docker, for instance, where it's host name is "backend").

## DoD CA Management

The certificate bundle is located in `ssl/server-certs/ca-chain.pem`. Currently, it contains the testing client CA along with all the DoD root and intermediate certs. If the bundle needs to be updated, run:

```
./script/sync-dod-certs
```

This will pull down all of the DoD CAs and add them to the bundle.

## DoD CRL Management

Before updating the CRLs, note that the CRL list is about 50MB and the connection is slow. To refresh the CRLs, run:

```
script/sync-crls
```

This will download and unpack the CRLs into a `crl` directory in the repo root. These are not track or used for development, but are necessary for production.
