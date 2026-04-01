from fastapi import FastAPI, Depends, status, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from Accounts.models import Account
from DateBase.db import get_session
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="accounts_app")

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

#создание счёта
@app.post("/create_account", status_code=status.HTTP_201_CREATED)
async def create_account(value: float = Form(...), session: AsyncSession = Depends(get_session)):
    account = Account(balance=value)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

@app.get("/accounts")
async def get_groups(session:AsyncSession = Depends(get_session)):
    accounts = await session.scalars(select(Account))
    return accounts.all()

@app.get("/get_account/{account_id}")
async def get_groups(account_id: int, session:AsyncSession = Depends(get_session)):
    account = await session.scalar(select(Account).where(Account.id==account_id))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account