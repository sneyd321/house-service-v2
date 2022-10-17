from models.db import DB
from models.repository import Repository
from models.models import House
from models.Firebase import Firebase
import asyncio, pytest, json

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()


@pytest.mark.asyncio
async def test_House_Service_returns_empty_list_when_landlord_id_does_not_exist():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open("./tests/sample_house.json", mode="r") as sample_house:
        houseData = json.load(sample_house)
        house = House(firebase, **houseData)
        house.landlord_id = 0
    
    monad = await repository.get_all_by_landlord_id(house)
    assert monad.get_param_at(0) == []

@pytest.mark.asyncio
async def test_House_Service_returns_error_when_house_key_does_not_exist():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open("./tests/sample_house.json", mode="r") as sample_house:
        houseData = json.load(sample_house)
        house = House(firebase, **houseData)
        house.houseKey = "111111"
    monad = await repository.get_house_by_house_key(house)
    assert monad.error_status == {"status": 404, "reason": "No data in repository monad"}

@pytest.mark.asyncio
async def test_House_Service_generates_a_new_key_when_a_duplicate_key_exists():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open("./tests/sample_house.json", mode="r") as sample_house:
        houseData = json.load(sample_house)
        house = House(firebase, **houseData)
        house.houseKey = "111111"

    house = await repository.generate_hash(house, ["111111"])
    assert house.houseKey != "111111"