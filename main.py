import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List
from models.schema import HouseSchema
from models.db import DB
from models.repository import Repository
from models.models import *
from kazoo.client import KazooClient
from kazoo.retry import KazooRetry
from fastapi_responses import custom_openapi

user = "root"
password = "root"
host = "localhost"
database = "roomr"

db = DB(user, password, host, database)
repository = Repository(db)

app = FastAPI()
#Converts HTTP Exception in swagger documentation
app.openapi = custom_openapi(app)
zk = KazooClient(hosts="host.docker.internal:2181", connection_retry=KazooRetry(ignore_expire=False))


@app.on_event("startup")
async def startup_event():
    try:
        await repository.create_all()
    except OperationalError:
        SystemExit()
    zk.start()
    if not zk.connected:
        zk.stop()
        raise Exception("Unable to connect to zookeeper.")
    zk.ensure_path("Services")
    if not zk.exists("Services/House-Service"):
        zk.create("Services/House-Service", ephemeral=True)
    zk.set("Services/House-Service", b"http://localhost:8082")

@app.post("/Landlord/{landlordId}/House")
async def create_house(landlordId: int, houseSchema: HouseSchema):
    house = House(landlordId, houseSchema.dict()["firebaseId"])
    monad = await repository.insert_house(house)
    if monad.error_status:
        return HTTPException(**monad.error_status)
    return house.to_json()


@app.get("/House/{houseId}", response_model=HouseSchema)
async def get_house_by_id(leaseId: int):
    landlordAddress = LandlordAddress(**landlordAddressSchema.dict())
    landlordAddress.lease_id = leaseId
    status = await repository.update_landlord_address(landlordAddress)
    if status == "OPERATIONAL_ERROR":
        raise HTTPException(status_code=502, detail="Could not connect to DB")
    return landlordAddress.to_json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)