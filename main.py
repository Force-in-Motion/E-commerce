from fastapi import FastAPI
from contextlib import asynccontextmanager

from service import engine
from service.database.models import Base
from web.item import router as item_router
from web.views.user import router as users_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.get_engine().begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

    yield



app = FastAPI(lifespan=lifespan)
app.include_router(item_router)
app.include_router(users_router)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
