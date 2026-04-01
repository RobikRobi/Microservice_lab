from fastapi import FastAPI, Depends, status, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Accounts.models import Account
from DateBase.db import get_session
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="fines_app")

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


@app.put("/get_account_fines/{account_id}")
async def get_account_10(account_id: int, 
                         fine: float, 
                         session:AsyncSession = Depends(get_session)):
    account = await session.scalar(select(Account).where(Account.id==account_id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    await session.refresh(account)
    account.balance = account.balance - account.balance * 0.1
    return account

