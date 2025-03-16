from auth import AuthHandler
from fastapi import FastAPI
from pydantic import BaseModel
from mosip_auth_sdk.models import DemographicsModel

server = FastAPI()
auth = AuthHandler()


class DemographicRequestData(BaseModel):
    uin: str


class AgeRequest(DemographicRequestData):
    age: int


class DobRequest(DemographicRequestData):
    dob: str

class OTPGenerationRequest(DemographicRequestData):
    ...

class OTPVerificationRequest(DemographicRequestData):
    txn_id: str
    otp_value: str


@server.get("/")
async def root():
    return {"serverName": "mosip-sdk-api"}


@server.post("/age/")
async def age(age_data: AgeRequest):
    demo_data = DemographicsModel(age=str(age_data.age))
    auth_response = auth.yesno(age_data.uin, demo_data)
    return {"authStatus": auth_response}


@server.post("/dob/")
async def dob(dob_data: DobRequest):
    demo_data = DemographicsModel(dob=dob_data.dob)
    auth_response = auth.yesno(dob_data.uin, demo_data)
    return {"authStatus": auth_response}

@server.post("/otp/")
async def otp(otp_data: OTPGenerationRequest):
    txn_id = auth.otp_request(otp_data.uin)
    return {"txn_id": txn_id}

@server.patch("/otp/")
async def patch_otp(otp_data: OTPVerificationRequest):
    auth_response = auth.otp_verify(otp_data.uin, otp_data.txn_id, otp_data.otp_value)
    return {"authStatus": auth_response}