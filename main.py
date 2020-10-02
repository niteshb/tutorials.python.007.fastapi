from typing import Optional
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    """
    display the stock screener dashboard / homepage
    """
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            "somevar": 2,
        },
    )

@app.post("/stock")
def create_stock():
    """creates a stock and stores it in the database

    Returns:
        [type]: [description]
    """
    return {
        "code": "success",
        "message": "stock created",
    }
