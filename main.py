import uvicorn, os
from fastapi import FastAPI, HTTPException
from models.schema import HouseSchema
from models.db import DB
from models.repository import Repository
from models.models import House
from models.Firebase import Firebase

user = os.environ.get("DB_USER", "root")
password = os.environ.get("DB_PASS", "root")
host = os.environ.get("DB_HOST", "localhost")
database = "roomr"

db = DB(user, password, host, database)
repository = Repository(db)

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

app = FastAPI()

@app.get("/Health")
async def health_check():
    return {"status": 200}

@app.post("/House")
async def create_house(request: HouseSchema):
    house = House(**request.dict())
    house.init_firebase(firebase)
    monad = await repository.insert(house)
    if monad.has_errors():
         return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return house.to_json()


@app.get("/Landlord/{landlordId}/House")
async def get_house_by_id(landlordId: int):
    house = House(landlordId=landlordId)
    monad = await repository.get_all_by_landlord_id(house)
    if monad.has_errors():
         return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [house.to_json() for house in monad.get_param_at(0)]
    

@app.get("/House/{houseKey}")
async def get_house_by_house_key(houseKey: str):
    house = House(landlordId=0)
    house.houseKey = houseKey
    monad = await repository.get_house_by_house_key(house)
    if monad.has_errors():
        return HTTPException(status_code=404, detail="Not found")
    return monad.get_param_at(0).to_json()

@app.delete("/House/{houseId}")
async def delete_house(houseId):
    house = House(0)
    house.id = houseId
    monad = await repository.delete(house, firebase)
    if monad.has_errors():
         return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return monad.get_param_at(0).to_json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8082)