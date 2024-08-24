# Food Services Fastapi Backend

Backend application to centralize services related to restaurant management, delivery, recipes, etc.

## Dependencies 
Python 3.11.9  
Docker 20.10 + docker-compose 2.12  
Postgres 16.0 (sourced on compose file)    
Redis 7.4.0 (sourced on compose file)  
Alembic 1.13.2 (sourced on requirements.txt)

## Setup
### Staging
`docker-compose -f docker-compose.staging.yml`