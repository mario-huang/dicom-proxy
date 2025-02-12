from fastapi import FastAPI
from pydantic import BaseModel
from echo_scu import echo_scu
from scu_event import SCUEvent


app = FastAPI()

class QueryParameters(BaseModel):
    includefield: str
    fuzzymatching: bool
    limit: int
    offset: int

@app.get("/echo")
async def echo():
    event = SCUEvent()
    echo_scu(event)
    return

@app.get("/studies")
async def studies():
    return