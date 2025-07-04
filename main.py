from fastapi import FastAPI
from contextlib import asynccontextmanager

from service.database.db_connection import db_connector
from service.database.models import Base
from web.views.user import router as users_router
from web.views.product import router as product_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_connector.get_engine().begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

    yield



app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
app.include_router(product_router)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
