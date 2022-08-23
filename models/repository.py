
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
            monad = MaybeMonad(house)
            monad = await monad.bind(self.db.insert)
            if monad.error_status:
                await self.db.rollback()
                return monad
            await self.db.commit()
            return monad
        

    async def get_all_by_homeowner_id(self, homeownerId):
        async with self.db.get_session():
            monad = MaybeMonad()
            await self.db.get_all_by_homeowner_id(House, homeownerId)
            await self.db.commit()
        

   