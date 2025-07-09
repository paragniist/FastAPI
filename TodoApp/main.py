from fastapi import FastAPI
from database import engine
import model
from router import auth,todos,admin,users
app = FastAPI(debug=True)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

model.base.metadata.create_all(bind=engine)
