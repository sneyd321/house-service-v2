import uvicorn, os
from fastapi import FastAPI, HTTPException
from typing import List
from models.schema import HouseSchema
from models.db import DB
from models.repository import Repository
from models.models import *
from fastapi_responses import custom_openapi

user = os.environ.get("MYSQL_USER", "root")
password = os.environ.get("MYSQL_PASS", "root")
host = os.environ.get("MYSQL_HOST", "localhost")
database = "roomr"

db = DB(user, password, host, database)
repository = Repository(db)

app = FastAPI()
#Converts HTTP Exception in swagger documentation
app.openapi = custom_openapi(app)


@app.on_event("startup")
async def startup_event():
    try:
        await repository.create_all()
    except OperationalError:
        SystemExit()
  

@app.get("/Health")
async def health_check():
    return {"status": 200}


@app.post("/House")
async def create_house(request: HouseSchema):
    house = House(**request.dict())
    monad = await repository.insert_house(house)
    if monad.error_status:
        return HTTPException(**monad.error_status)
    return house.to_json()


@app.get("/Landlord/{landlordId}/House")
async def get_house_by_id(landlordId: int):
    houses = await repository.get_all_by_landlord_id(landlordId)
    return [house.to_json() for house in houses]
    

@app.get("/House/{houseKey}")
async def get_house_by_house_key(houseKey: str):
    house = await repository.get_house_by_house_key(houseKey)
    if not house:
        return HTTPException(status_code=404, detail="Not found")
    return house.to_json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)