from fastapi import FastAPI, Depends, status, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Accounts.models import Account
from Bonuses.shema import BonusUpdate
from DateBase.db import get_session
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="bonus_app")

origins = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type",
                   "Set-Cookie",
                   "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.put("/get_account_bonuses/{account_id}")
async def get_account_bonus(account_id: int, 
                         bonus_data: BonusUpdate, 
                         session:AsyncSession = Depends(get_session)):
    account = await session.scalar(select(Account).where(Account.id==account_id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    await session.refresh(account)
    account.bonuses += bonus_data.bonuses
    await session.commit()
    return account

@app.put("/accrue_bonuses/{account_id}")
async def get_accrue_bonuses(account_id: int,
                             session:AsyncSession = Depends(get_session)):
    account = await session.scalar(select(Account).where(Account.id == account_id))

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if account.bonuses == 0:
        raise HTTPException(status_code=400, detail="You have no accrued bonuses")
    
    account.balance += account.bonuses
    account.bonuses = 0

    await session.commit()
    return account
