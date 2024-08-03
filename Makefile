test:
	docker compose up -d redis
	pytest
	docker compose down redis