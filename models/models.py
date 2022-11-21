
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
import string
import random

Base = declarative_base()

class House(Base):
    __tablename__ = "house"

    id = Column(Integer(), primary_key=True)
    landlord_id = Column(Integer(), nullable=False)
    houseKey = Column(String(10), nullable=False, unique=True)
    firebaseId = Column(String(100), nullable=False)

    def __init__(self, landlordId):
        self.landlord_id = landlordId
        
    def init_firebase(self, firebase):
        self.firebase = firebase
        self.firebaseId = self.firebase.get_firebase_id()

  
       
    def generate_hash(self):
        self.houseKey = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def to_dict(self):
        return {
            "landlordId": self.landlord_id,
            "houseKey": self.houseKey,
            "firebaseId": self.firebaseId
        }

    def to_json(self):
        return {
            "id": self.id,
            "landlordId": self.landlord_id,
            "houseKey": self.houseKey,
            "firebaseId": self.firebaseId
        }

