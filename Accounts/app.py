from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session
from Accounts.models import Account
from DateBase.db import get_session



app = FastAPI(title="accounts_app")

#создание счёта
@app.post("/create_account", status_code=status.HTTP_201_CREATED)
def create_account(value: float, session: Session = Depends(get_session)):
    print(value)
    account = Account(balance=value)
    print(account)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account