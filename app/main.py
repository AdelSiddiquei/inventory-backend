from fastapi import FastAPI
import psycopg

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Congrats, you  launched a server"}


@app.get("/ping")
async def ping():
    return {"message": "Ping endpoint functioning"}

app.put("/inventory")
def new_item():
    pass