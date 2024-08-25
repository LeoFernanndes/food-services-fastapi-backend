# Food Services Fastapi Backend

Backend application to centralize services related to restaurant management, delivery, recipes, etc.  
![Api docs image](https://drive.google.com/file/d/1oPS0CMFyaEPzrnWnng0ka9whX9Tef86C/view)


## Dependencies 
Python 3.11.9  
Docker 20.10 + docker-compose 2.12  
Postgres 16.0 (sourced on compose file)    
Redis 7.4.0 (sourced on compose file)  
Alembic 1.13.2 (sourced on requirements.txt)

## Setup
### Staging
Before starting, be sure ports 8000 for api, 5432 for postgres and 6379 for redis are available.  
`docker-compose -f docker-compose.staging.yml`

### Development
Before starting, be sure ports 5432 for postgres and 6379 for redis are available.  
1. Spin up backing services:  
   `docker-compose -f docker-compose.dev.yml`
2. (optional) Create a virtual environment:  
   `python3 -m venv venv`
3. Install python depencies:  
   `pip install -r requirements.txt`
4. Export root path as PYTHONPATH.  
   On ubuntu, for example, `export PYTHONPATH=$(pwd)`
5. Run api:  
   `python3 ./presentation/http/fastapi/main.py`