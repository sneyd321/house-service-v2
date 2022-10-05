
from sqlalchemy.exc import OperationalError, IntegrityError
from models.models import *
from models.monad import MaybeMonad

class Repository:

    def __init__(self, db):
        self.db = db

    async def create_all(self):
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await self.db.commit()

    async def insert_house(self, house):
        async with self.db.get_session():
            house.generate_hash()
            existingKeys = await self.db.get_all_house_keys(house.id)
            while house.houseKey in existingKeys:
                house.houseKey = house.generate_hash()

            monad = MaybeMonad(house)
            monad = await monad.bind(self.db.insert)
            if monad.error_status:
                await self.db.rollback()
                return monad
            await self.db.commit()
            return monad
        

    async def get_all_by_landlord_id(self, landlord_id):
        async with self.db.get_session():
            houses = await self.db.get_all_by_landlord_id(landlord_id)
            await self.db.commit()
            return houses
        
    async def get_house_by_house_key(self, houseKey):
        async with self.db.get_session():
            house = await self.db.get_house_by_house_key(houseKey)
            await self.db.commit()
            return house

   