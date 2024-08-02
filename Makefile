test:
	docker compose up -d
	export PYTHONPATH=$(pwd)
	pytest
	docker compose down