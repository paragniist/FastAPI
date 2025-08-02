from fastapi import FastAPI,Request,status,HTTPException,Depends
from .database import engine
from .model import base
from .router import auth,todos,admin,users
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")
templates = Jinja2Templates(directory="TodoApp/templates")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

base.metadata.create_all(bind=engine)
