from typing import Set, Union, List
from pydantic import BaseModel

class HouseSchema(BaseModel):
    landlordId: int
   
class TenantAccountCreatedNotificationSchema(BaseModel):
    firstName: str
    lastName: str
    email: str
    houseKey: str