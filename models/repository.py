from models.monad import RepositoryMaybeMonad

class Repository:

    def __init__(self, db):
        self.db = db


    async def commit(self, house):
        await self.db.commit()

    async def generate_hash(self, house, houseKeys):
        while house.houseKey in houseKeys:
                house.houseKey = house.generate_hash()
        return house

    async def insert(self, house):
        async with self.db.get_session():
            house.generate_hash()
            monad = await RepositoryMaybeMonad(house) \
                .bind_data(self.db.get_all_house_keys)
            if monad.has_errors():
                print(monad.error_status)
                return monad
            
            monad = await RepositoryMaybeMonad(house, monad.get_param_at(0)) \
                .bind_data(self.generate_hash)
               
            monad = await RepositoryMaybeMonad(house) \
                .bind(self.db.insert)
            if monad.has_errors():
                await self.db.rollback()
            else:
                await self.db.commit()
            return monad

    async def delete(self, house, firebase):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(house) \
                .bind_data(self.db.get_house_by_id)
            houseFromDB = monad.get_param_at(0)
            if houseFromDB is None:
                return RepositoryMaybeMonad(None, error_status={"status": 404, "reason": f"House not found with id {house.id}"})
            
            firebase.delete_document(houseFromDB.firebaseId)
            monad = await RepositoryMaybeMonad(houseFromDB) \
                .bind(self.db.delete)
            if monad.has_errors():
                await self.db.rollback()
            else:
                await self.db.commit()
            return monad
        

    async def get_all_by_landlord_id(self, house):
        async with self.db.get_session():
            return await RepositoryMaybeMonad(house) \
                .bind_data(self.db.get_all_by_landlord_id)
            
          
        
    async def get_house_by_house_key(self, house):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(house) \
                .bind_data(self.db.get_house_by_house_key)
            if monad.has_errors():
                self.db.rollback()
                return monad
            return await monad.bind(self.commit)
          

   