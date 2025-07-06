from fastapi import FastAPI
from contextlib import asynccontextmanager


from web.views import include_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
include_router(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
