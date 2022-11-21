from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from models.models import House

class DB:

    def __init__(self, user, password, host, database):
        self.engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{database}", pool_pre_ping=True)
        Session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = Session()
        
    def get_session(self):
        return self.session
        
    async def get(self, model, id):
        result = await self.session.execute(select(model).where(model.id == id))
        return result.scalars().first()

    async def get_all_by_landlord_id(self, house):
        result = await self.session.execute(select(House).where(House.landlord_id == house.landlord_id))
        return result.scalars().all()

    async def get_all_house_keys(self, house):
        result = await self.session.execute(select(House.houseKey).where(House.id == house.id))
        return result.scalars().all()

    async def get_house_by_house_key(self, house):
        result = await self.session.execute(select(House).where(House.houseKey == house.houseKey))
        return result.scalars().first()

    async def get_house_by_id(self, house):
        result = await self.session.execute(select(House).where(House.id == house.id))
        return result.scalars().first()

    async def insert(self, data):
        self.session.add(data)

    async def delete(self, data):
        await self.session.execute(delete(House).where(House.id == data.id))
            
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
    
 
    