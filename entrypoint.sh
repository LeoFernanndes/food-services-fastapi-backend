#!/bin/bash

alembic upgrade head
python ./presentation/http/fastapi/main.py