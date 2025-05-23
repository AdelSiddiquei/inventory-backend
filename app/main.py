from dotenv import load_dotenv

load_dotenv()

import os
from fastapi import FastAPI, HTTPException, Request
import psycopg
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Congrats, you  launched a server"}


@app.get("/ping")
async def ping():
    return {"message": "Ping endpoint functioning"}


class InventoryRequest(BaseModel):
    item: str
    description: str
    price: float


class TransactionsPost(BaseModel):
    item: str
    quantity: int

class TransactionsPatch(BaseModel):
    uuid: UUID
    item: str
    quantity: int


# Inventory endpoints
@app.post("/inventory")
def new_item(body: InventoryRequest):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                query = f"INSERT INTO inventory (item, description, price) VALUES ('{body.item}', '{body.description}', {body.price})"
                cursor.execute(query)
            return {
                "data": {
                    "message": "Added successfully",
                    "item": body.item,
                    "description": body.description,
                    "price": body.price,
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")


@app.get("/inventory")
def get_items():
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        ) as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM inventory;"
                cursor.execute(query)
                data = cursor.fetchall()

        return {"data": {"inventory": data}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")


@app.delete("/inventory/{item}")
def remove_item(item):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                query = f"DELETE FROM inventory WHERE item = '{item}'"
                cursor.execute(query)
                if cursor.rowcount == 0:
                    return {
                        "data": {"message": f"Item '{item}' not found, nothing deleted"}
                    }

        return {"data": {"message": "Delete successful", "item": item}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")


@app.patch("/inventory")
def update_item(body: InventoryRequest):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                query = f"UPDATE inventory SET description = '{body.description}', price = {body.price} WHERE item = '{body.item}';"
                cursor.execute(query)
                if cursor.rowcount == 0:
                    return {
                        "data": {
                            "message": f"Item '{body.item}' not found, nothing updated"
                        }
                    }

        return {
            "data": {
                "message": "Update successful",
                "item": body.item,
                "description": body.description,
                "price": body.price,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")


# Transactions endpoints
@app.post("/transactions")
def new_order(body: TransactionsPost):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                query = f"INSERT INTO transactions (item, quantity) VALUES ('{body.item}', {body.quantity}) RETURNING transaction_id"
                cursor.execute(query)
                transaction_id = cursor.fetchone()[0]
            return {
                "data": {
                    "message": "Added successfully",
                    "transaction_id": str(transaction_id),
                    "item": body.item,
                    "quantity": body.quantity,
                }
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")


@app.get("/transactions")
def get_orders():
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        ) as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM transactions;"
                cursor.execute(query)
                data = cursor.fetchall()

        return {"data": {"transactions": data}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")


@app.delete("/transactions/{transaction_id}")
def remove_order(transaction_id):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                query = f"DELETE FROM transactions WHERE transaction_id = {transaction_id}"
                cursor.execute(query)
                if cursor.rowcount == 0:
                    return {
                        "data": {"message": f"Item '{item}' not found, nothing deleted"}
                    }

        return {"data": {"message": "Delete successful", "transaction_id": transaction_id}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")


@app.patch("/transactions")
def update_order(body: TransactionsPatch):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            autocommit=True,
        ) as conn:
            with conn.cursor() as cursor:
                query = f"UPDATE transactions SET quantity = {body.quantity}, item = '{body.item}' WHERE transaction_id = '{body.uuid}';"
                cursor.execute(query)
                if cursor.rowcount == 0:
                    return {
                        "data": {
                            "message": f"Transaction '{body.uuid}' not found, nothing updated"
                        }
                    }

        return {
            "data": {
                "message": "Update successful",
                "transaction_id": body.uuid,
                "item": body.item,
                "quantity": body.quantity,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"There was an error: {str(e)}")
