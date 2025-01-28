from fastapi import FastAPI
from pydantic import BaseModel

server = FastAPI()


class DemographicRequestData(BaseModel):
    uin: str


class AgeRequest(DemographicRequestData):
    age: int


class DobRequest(DemographicRequestData):
    dob: str


@server.get("/")
async def root():
    return {"message": "Hello, world!"}
