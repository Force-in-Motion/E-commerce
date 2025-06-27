from fastapi import FastAPI
from web.item import router as item_router
from web.users.views import router as users_router


app = FastAPI()
app.include_router(item_router)
app.include_router(users_router)




if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', reload=True)
