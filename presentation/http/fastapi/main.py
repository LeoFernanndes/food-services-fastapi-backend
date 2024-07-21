import logging
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI

from presentation.http.fastapi.routers.user import user_router
from presentation.http.fastapi.routers.auth import auth_router


# TODO: check if it is possible to use ormmodel capabilities to get a parsed integrity error handler on repositories
# TODO: check if it is possible to add database definitions on domain model to be implemented in the orm models
# TODO: find a way of running testcontainers on the image building to user it as part of a ci pipeline

load_dotenv()
logger = logging.getLogger(__name__)

app = FastAPI(root_path="")
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload_excludes=["./database/*"])
