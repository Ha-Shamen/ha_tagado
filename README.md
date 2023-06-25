# Tagado home assignment

## Structure
- The project consists of three services
    - mongodb
    - tagadoservice - web-service:1.0.0
    - tagadodataservice - data-service:1.0.0
- Each service is designed to be deployed as a micro service defined in:
    - docker-compose.yaml
- Code is located in each service folder 
- Each service has it own Dockerfile for deployment instructions

## Development
- The whole project can be deployed in a Docker container defined in the root folder
- Run poetry install on root to get all the necessary packages

## Deployment
- Docker installed is required.
- Navigate to the project root and execute:
    - Start -
        `docker-compose -f ./docker-compose.yaml up -d`
    - Stop -
        `docker-compose -f ./docker-compose.yaml stop`

## Runtime
- Web service access point is localhost:7000
- You can use swagger to examine and test the service

## To discuss
- Unit tests were not created
- MongoService should be defined in the utils and used by both services
- flake8 or any other code format tools were used