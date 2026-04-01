import httpx
from fastapi import FastAPI
from binascii import Error
from DateBase.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from Accounts.models import Account




app = FastAPI(title="main_app")
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

@app.get("/")
async def create_db():
    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.drop_all)
        except Error as e:
            print(e)     
        await  conn.run_sync(Base.metadata.create_all)
    return({"msg":"True"})


@app.post("/create_account")
async def create_account(url: str, value: float):
    async with httpx.AsyncClient() as client:
        form_data = {"value": value}
        print(form_data)
        response = await client.post(url=url, data=form_data)
        return response.json()
