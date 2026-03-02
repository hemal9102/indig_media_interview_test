//here we will give core logic
from fastapi  import FastAPI , Depends , Request , Form
from Fastapi.responses import HTMLResponse , RedirectResponse

from sqlalchemy.orm import Session
import models, database


# making databse table 
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title = "Online test system ")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
