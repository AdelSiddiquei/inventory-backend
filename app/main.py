from dotenv import load_dotenv

load_dotenv()

import os
from fastapi import FastAPI, HTTPException, Request
import psycopg
from pydantic import BaseModel

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

class TransactionsRequest(BaseModel):
    item: str
    quantity: int



# Inventory endpoints
@app.post("/inventory/")
def new_item(body: InventoryRequest):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        ) as conn:
            conn.autocommit = True
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
        return HTTPException(500, "There was an error, try again later.")


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
        return HTTPException(500, "There was an error, try again later.")


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

        return {
            "data": {
                "message": "Delete successful",
                "item": item,
                "description": description,
                "price": price,
            }
        }
    except Exception as e:
        return HTTPException(500, "There was an error, try again later.")


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

        return {"data": {"message": "Update successful", "item": body.item, "description": body.description, "price": body.price}}
    except Exception as e:
        return HTTPException(500, "There was an error, try again later.")


# Transactions endpoints
@app.post("/transactions/")
def new_order(body: TransactionsRequest):
    try:
        with psycopg.connect(
            dbname=os.getenv("POSTGRES_DBNAME"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        ) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                query = f"INSERT INTO transactions (item, quantity) VALUES ('{body.item}', {body.quantity})"
                cursor.execute(query)
            return {
                "data": {
                    "message": "Added successfully",
                    "item": body.item,
                    "quantity": body.quantity,
                }
            }
    except Exception as e:
        return HTTPException(500, "There was an error, try again later.")


@app.get("/transactions")
def get_orders(table_name: str):
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
        return HTTPException(500, "There was an error, try again later.")


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
                query = f"DELETE FROM transactions WHERE transaction_id = '{transaction_id}'"
                cursor.execute(query)

        return {
            "data": {
                "message": "Delete successful",
                "item": item,
                "description": description,
                "price": price,
            }
        }
    except Exception as e:
        return HTTPException(500, "There was an error, try again later.")


# @app.put("/transactions")
# def update_order():
#     pass
