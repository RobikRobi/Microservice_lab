from fastapi import FastAPI, Depends, status, Form
from sqlalchemy.orm import Session
from Accounts.models import Account
from DateBase.db import get_session
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="accounts_app")

origins = [
    "http://localhost:8000",
    "http://localhost:8001",
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
async def create_account(value: float = Form(...), session: Session = Depends(get_session)):
    print(value)
    account = Account(balance=value)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account