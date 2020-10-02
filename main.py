from typing import Optional
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
import yfinance

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
def home(
        request: Request,
        db: Session = Depends(get_db),
    ):
    """
    display the stock screener dashboard / homepage
    """
    stocks = db.query(Stock)
    
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            "stocks": stocks,
        },
    )

def fetch_stock_data(id: int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()

    yahoo_data = yfinance.Ticker(stock.symbol)
    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    dividend = yahoo_data.info['dividendYield']
    stock.dividend_yield = 0 if dividend == None else dividend * 100

    db.add(stock)
    db.commit()
    print('    Data fetched from Yahoo!Finance and saved for', stock.symbol)

@app.post("/stock")
async def create_stock(
        stock_request: StockRequest, 
        background_tasks: BackgroundTasks, 
        db: Session = Depends(get_db)
    ):
    """creates a stock and stores it in the database

    Returns:
        [type]: [description]
    """
    stock = Stock()
    stock.symbol = stock_request.symbol
    db.add(stock)
    db.commit()

    background_tasks.add_task(fetch_stock_data, stock.id)

    return {
        "code": "success",
        "message": "stock created",
    }
