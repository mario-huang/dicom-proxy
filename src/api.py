from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Attributes(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

class QueryParameters(BaseModel):
    includefield: str
    fuzzymatching: bool
    limit: int
    offset: int

@app.get("/studies")
async def studies():
    return