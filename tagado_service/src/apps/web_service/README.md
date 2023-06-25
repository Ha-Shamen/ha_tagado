# Tagado web service

## Structure
- Dockerfile - Contains all that is needed to deploy the service as standalone
    - Assuming there is mongodb service
- Poetry was used for package management
- app - Contains the logic

## Design
- Project is using FastAPI for all web interactions
- It is possible to utilize FastAPI swagger for test or discovery
- All input variables are sent in url and not body
- If you wish to replace the default MongoDb a connection string can be defined as environment variable MONGOSERVICE
- If no such variable then the default, as defined in docker-compose.yaml, is used
- The service assumes the neccesary collections were created by the data service
- Excpected dates are in format of Y-M-d
- Search for comments can be done in two ways
    - simple - calling the source web service for data
    - mongodb - will return only the text and not the whole comment 
- I expanded the api to get also post data by id in order to test the update entry point