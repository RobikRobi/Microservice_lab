import httpx
from fastapi import FastAPI
from binascii import Error
from DateBase.db import engine, Base




app = FastAPI(title="main_app")


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
