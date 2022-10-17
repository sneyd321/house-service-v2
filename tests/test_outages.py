from models.db import DB
from models.repository import Repository
from models.models import House
from models.Firebase import Firebase
import asyncio, pytest, json

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

@pytest.mark.asyncio
async def test_House_Service_returns_an_error_during_database_outage():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open("./tests/sample_house.json", mode="r") as sample_house:
        houseData = json.load(sample_house)
        house = House(firebase, **houseData)
    monad = await repository.insert(house)
    assert monad.error_status == {"status": 502, "reason": "Failed to connect to database"}