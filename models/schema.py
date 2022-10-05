from typing import Set, Union, List
from pydantic import BaseModel

class HouseSchema(BaseModel):
    landlordId: int
   