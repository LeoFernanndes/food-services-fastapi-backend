import logging
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI

from presentation.http.fastapi.routers.user import user_router


load_dotenv()
logger = logging.getLogger(__name__)

app = FastAPI(root_path="/api")
app.include_router(user_router, prefix="/users")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload_excludes=["./database/*"])
