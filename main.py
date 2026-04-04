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
    "http://localhost:8002",
    "http://localhost:8003",
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
async def create_account_url(url: str, value: float):
    async with httpx.AsyncClient() as client:
        form_data = {"value": value}
        response = await client.post(url=url, data=form_data)
        response.raise_for_status()

        return response.json()

@app.get("/accounts")
async def create_account_url(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url)
        response.raise_for_status()

        return response.json()
    
@app.get("/get_account")
async def create_account_url(url: str, account_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=f"{url}/{account_id}")
        response.raise_for_status()

        return response.json()
    
@app.put("/get_account_fines")
async def get_account_fines_url(url: str, account_id: int, fine):
    async with httpx.AsyncClient() as client:
        target_url = f"{url}/{account_id}"
        params = {"fine": fine}
        response = await client.put(target_url, json=params)
        response.raise_for_status()

        return response.json()

@app.put("/get_account_bonuses")
async def get_account_bonuses_url(url: str, account_id: int, bonus):
    async with httpx.AsyncClient() as client:
        target_url = f"{url}/{account_id}"
        params = {"bonuses": bonus}
        response = await client.put(target_url, json=params)
        response.raise_for_status()

        return response.json()
    
@app.put("/accrue_bonuses")
async def get_accrue_bonuses_url(url: str, account_id: int):
    async with httpx.AsyncClient() as client:
        target_url = f"{url}/{account_id}"
        response = await client.put(target_url)

        try:
            response = await client.put(target_url)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            return {
                "error": "Remote service error",
                "status_code": e.response.status_code,
                "details": e.response.json()
            }