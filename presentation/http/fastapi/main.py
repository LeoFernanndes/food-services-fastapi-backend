import logging
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from presentation.http.fastapi.routers.user import user_router
from presentation.http.fastapi.routers.auth import auth_router


# TODO: check if it is possible to use ormmodel capabilities to get a parsed integrity error handler on repositories
# TODO: check if it is possible to add database definitions on domain model to be implemented in the orm models
# TODO: find a way of running testcontainers on the image building to user it as part of a ci pipeline

load_dotenv()
logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "auth",
        "description": "Authentication logic.",
    },
]

app = FastAPI(root_path="", title="Food Services Api", openapi_tags=tags_metadata)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload_excludes=["./database/*"])
