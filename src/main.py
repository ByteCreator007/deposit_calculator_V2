from dateutil.relativedelta import relativedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from datetime import datetime
from calendar import monthrange
from databases import Database
from sqlalchemy import MetaData, insert
from sqlalchemy.ext.asyncio import create_async_engine
from src.models import metadata, deposits
from src.config import settings
import json
import asyncio

app = FastAPI()

DATABASE_URL = settings.database_url

database = Database(DATABASE_URL)
metadata = MetaData()

async_engine = create_async_engine(DATABASE_URL, echo=True)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class DepositRequest(BaseModel):
    date: str = Field(..., pattern=r"^\d{2}\.\d{2}\.\d{4}$", description="Дата в формате dd.mm.yyyy")
    periods: int = Field(..., ge=1, le=60, description="Количество месяцев по вкладу (от 1 до 60)")
    amount: int = Field(..., ge=10000, le=3000000, description="Сумма вклада (от 10 000 до 3 000 000)")
    rate: float = Field(..., ge=1, le=8, description="Процентная ставка (от 1 до 8)")

@app.post("/calculate")
async def calculate_deposit(request: DepositRequest) -> Dict[str, float]:
    try:
        start_date = datetime.strptime(request.date, "%d.%m.%Y")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неверный формат даты")

    results = {}
    amount = request.amount
    last_day_of_month = monthrange(start_date.year, start_date.month)[1]
    if start_date.day == last_day_of_month:
        amount += amount * (request.rate / 100) / 12

    results[start_date.strftime("%d.%m.%Y")] = round(amount, 2)

    for period in range(1, request.periods):
        next_date = start_date + relativedelta(months=period)
        amount += amount * (request.rate / 100) / 12
        results[next_date.strftime("%d.%m.%Y")] = round(amount, 2)


    query = insert(deposits).values(
        date=request.date,
        periods=request.periods,
        amount=request.amount,
        rate=request.rate,
        result=json.dumps(results)
    )
    await database.execute(query)

    return results