from typing import Optional
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
from database import SessionLocal, engine
from models import Stock

class StockRequest(BaseModel):
    symbol: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

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
def create_stock(stock_request: StockRequest, db: Session = Depends(get_db)):
    """creates a stock and stores it in the database

    Returns:
        [type]: [description]
    """
    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()
    
    return {
        "code": "success",
        "message": "stock created",
    }
