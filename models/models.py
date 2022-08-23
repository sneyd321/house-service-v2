
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import OperationalError, IntegrityError
import hashlib



Base = declarative_base()

class House(Base):
    __tablename__ = "house"

    id = Column(Integer(), primary_key=True)
    landlord_id = Column(Integer(), nullable=False)
    firebaseId = Column(String(100), nullable=False)

    def __init__(self, landlordId, firebaseId):
        self.landlord_id = landlordId
        self.firebaseId = firebaseId

    def generate_hash(self, houseId):
        h = hashlib.sha3_512() 
        b = str(houseId).encode("utf-8")
        h.update(b)
        return h.hexdigest()[:6]

    def to_dict(self):
        return {
            "houseKey": self.generate_hash(self.id),
            "firebaseId": self.firebaseId
        }

    def to_json(self):
        return {
            "id": self.id,
            "houseKey": self.generate_hash(self.id),
            "firebaseId": self.firebaseId
        }

