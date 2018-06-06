# authnid

[![Build Status](https://travis-ci.org/dod-ccpo/authnid.svg?branch=master)](https://travis-ci.org/dod-ccpo/authnid)

## Back end local development

* Update your local `hosts` file, set the IP `127.0.0.1` (your `localhost`) to `dev.cac.atat.codes`. The `docker-compose.override.yml` file will set the environment variable `SERVER_NAME` to that host. Otherwise you would receive 404 errors.

* Modify your hosts file, probably in `/etc/hosts` to include:

```
0.0.0.0    dev.cac.atat.codes
```

...that will make your browser talk to your locally running server.

* Start the stack with Docker Compose:

```bash
docker-compose up -d
```

* Your OS will handle redirecting `dev.cac.atat.codes` to your local stack. So, in your browser, go to: http://dev.cac.atat.codes.

The `docker-compose.override.yml` file for local development has a host volume with your app files inside the container for rapid iteration. So you can update your code and it will be the same code (updated) inside the container. You just have to restart the server, but you don't need to rebuild the image to test a change. Make sure you use this only for local development. Your final production images should be built with the latest version of your code and do not depend on host volumes mounted.

### Back end tests

To test the back end run:

```bash
# Start and build the testing stack
docker-compose up -d --build
sleep 20; # Give some time for the DB and prestart script to finish
# Run the REST tests
docker-compose exec -T backend-tests pytest
# Stop and eliminate the testing stack
docker-compose down -v --remove-orphans
```

**NOTE:** For the tests to run, they need to know the location of:

- the server's certificate authority (`ssl/certificate-authority/ca.crt`), set in the testing docker container with teh `REQUESTS_CA_BUNDLE` env variable
- the client public cert and private key, both in `ssl/client-certs/`

The tests run with Pytest, modify and add tests to `./tests/`.

### SSL Certificates

The `ssl` directory contains example certs for configuring the regular server SSL, client authentication, and the client certificates currently written to the sample PIVKey. It also contains a script, `make-certs.sh`, which can be used to write a new certificate authority and sign a CSR for the server SSL. The script writes the CSR to list multiple valid hosts (`subjectAltName`) so that the final cert can work across environments (like docker, for instance, where it's host name is "backend").
