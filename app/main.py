from fastapi import FastAPI
from utils import DBTools

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Congrats, you  launched a server"}


@app.get("/ping")
async def ping():
    return {"message": "Ping endpoint functioning"}

@app.put("/inventory")
def new_stock():
    pass

@app.get("/inventory")
def get_inventory():
    dbsession = DBTools()
    dbsession.get_table_as_array('inventory')