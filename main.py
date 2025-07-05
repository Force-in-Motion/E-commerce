from fastapi import FastAPI
from contextlib import asynccontextmanager

from service.database import db_connector
from service.database.models import Base
from web.views import include_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_connector.get_engine().begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

    yield



app = FastAPI(lifespan=lifespan)
include_router(app)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
