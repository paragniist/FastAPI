from fastapi import FastAPI
from .database import engine
from .model import base
from .router import auth,todos,admin,users
from fastapi.staticfiles import StaticFiles
app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")



app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

base.metadata.create_all(bind=engine)
