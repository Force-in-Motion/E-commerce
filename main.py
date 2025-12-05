import uvicorn
from fastapi import FastAPI

from app.view import include_router

app = FastAPI()
include_router(app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
