import uvicorn
from fastapi import FastAPI

from app.api.view.user import include_user_routers
# from app.api.view.admin import include_admin_routers

app = FastAPI()
include_user_routers(app)
# include_admin_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
