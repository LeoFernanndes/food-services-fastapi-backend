test:
	docker compose -f docker-compose.dev.yml up -d redis
	pytest
	docker compose -f docker-compose.dev.yml down redis