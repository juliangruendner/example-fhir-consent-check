# example-fhir-consent-check

This respository is meant to demonstrate how patients ids can be extracted from a fhir server using fhir search and how they can be potentially
used in subsequent queries

To test this you will need docker and docker-compose and python3 installed on your machine.

## How to use

- Start up the blaze fhir server - `docker-compose up -d`
- Wait for the server to start up - you can check in your browser if it is started up - `http://localhost:8081/fhir/Patient`
- Initialise the testdata - `bash init-testdata.sh`
- execute the example data extraction script - `python3 consent-check.py`