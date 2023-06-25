# Tagado data service

## Structure
- Dockerfile - Contains all that is needed to deploy the service as standalone
    - Assuming there is mongodb service
- Poetry was used for package management
- app - Contains the logic

## Design
- WAIT_TIME_SECONDS is an environment variable to decide what is the interval for pulling data
- If WAIT_TIME_SECONDS is not defined a defualt of 60 (seconds) is assigned
- If you wish to replace the default MongoDb a connection string can be defined as environment variable MONGOSERVICE
- If no such variable then the default, as defined in docker-compose.yaml, is used
