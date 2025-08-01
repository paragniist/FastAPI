from fastapi import APIRouter,Depends,Path,Query,HTTPException,Request
from ..model import Todos
from sqlalchemy.orm import Session
from typing import Annotated
from ..database import SessionLocal
from sqlalchemy.testing.pickleable import User
from starlette import status
from pydantic import BaseModel,Field
from .auth import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/todos",
    tags=["todos"]
)

class Todorequest(BaseModel):
    title:str = Field(min_length=5)
    description:str = Field(min_length=5)
    priority:int = Field(gt=0,lt=6)
    complete:bool = Field(default=True)

    model_config={
        "json_schema_extra":{
            "example":{
                "title":"TodoRequest",
                "description":"TodoRequest description",
                "priority":1,
                "complete":False
            }
        }
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency =  Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
templates = Jinja2Templates(directory="TodoApp/templates")

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response


##Pages##
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        access_token = request.cookies.get("access_token")
        user = await get_current_user(access_token)
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        return templates.TemplateResponse("todo.html", {"request": request, "todos": todos, "user": user})

    except Exception as e:
        print("Error in /todo-page:", e)
        import traceback
        traceback.print_exc()
        return redirect_to_login()

###Endpoint####
@router.get("/read_all")
async def read_all(user:user_dependency,db : db_dependency):
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get("/read_todos_by_id/{todo_id}",status_code=status.HTTP_200_OK)
async def read_by_id(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404,detail='AUTHENTICATION FAILED')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404,detail='Todo not found')

@router.post("/creating_todo",status_code=status.HTTP_201_CREATED)
async def create_todos(user:user_dependency,db : db_dependency,todo_request:Todorequest):
    if user is None:
        raise HTTPException(status_code=404,detail='AUTHENTICATION FAILED')
    todo_model = Todos(**todo_request.model_dump(),owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    return 'Successfully created a todo task'

@router.put("/updating_todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(user:user_dependency,db:db_dependency,todo_request:Todorequest,todo_id:int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()
    if user is None:
        raise HTTPException(status_code=404, detail='AUTHENTICATION FAILED')
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/selecting_todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def deleting_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=404, detail='AUTHENTICATION FAILED')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id==user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail="Todo not found")
    db.query(Todos).filter(Todos.id==todo_id).filter(Todos.owner_id==user.get('id')).delete()
    db.commit()