from fastapi import FastAPI
from fastapi.responses import JSONResponse

from dbms.db import DatabaseManager
import gpay_transactions_api

import numpy as np
from fastapi import File
from typing import Annotated

from pydantic import BaseModel

app = FastAPI()
database_manager = DatabaseManager()
app.include_router(gpay_transactions_api.router)


@app.get("/")
def read_root():
    return JSONResponse({
        "response": "Hello World"
    })


@app.get("/urls")
def url_schema():
    return app.openapi().get("paths")


@app.get("/user/authorize")
def authorize(userid: int, password: str):
    creds = database_manager.fetch_user(userid=userid)
    print(creds)
    if not creds:
        return JSONResponse({
            "code": 1,
            "response": "User not found"
        })
    if creds.password != password:
        return JSONResponse({
            "userid": userid
        })
    else:
        return JSONResponse({
            "code": 0,
            "userid": userid
        })


@app.get("/user/register")
def register(userid: int, password: str):
    creds = database_manager.fetch_user(userid=userid)
    if creds:
        return JSONResponse({
            "code": -1,
            "response": "User already exists"
        })
    else:
        database_manager.add_user(userid=userid, password=password)
        return JSONResponse({
            "code": 0,
        })


@app.get("/transactions/get")
def fetch_transactions(userid: int = None, methodid: int = None):
    transactions = database_manager.fetch_transaction(userid=userid, methodid=methodid)
    return JSONResponse({
        "code": 0,
        "transactions": [transaction.to_dict() for transaction in transactions]
    })


@app.get("/transactions/get")
def fetch_transactions(userid: int = None, methodid: int = None):
    transactions = database_manager.fetch_transaction(userid=userid, methodid=methodid)
    return JSONResponse({
        "code": 1,
        "transactions": [transaction.to_dict() for transaction in transactions]
    })


@app.get("/transactions/add")
def add_transaction(userid: int, methodid: int, amount: float):
    database_manager.add_transaction(userid=userid, methodid=methodid, amount=amount)
    return JSONResponse({
        "code": 0
    })


class Amounts(BaseModel):
    amounts: list


@app.post("/transactions/add_gpay")
def add_gpay_transaction(userid: int, amounts: Amounts):
    amounts = amounts.amounts
    for amount in amounts:
        database_manager.add_transaction(userid=userid, methodid=1, amount=amount)
    return JSONResponse({
        "code": 0
    })


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
