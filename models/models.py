
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import OperationalError, IntegrityError
import string
import random
from models.Firebase import Firebase


firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()
Base = declarative_base()

class House(Base):
    __tablename__ = "house"

    id = Column(Integer(), primary_key=True)
    landlord_id = Column(Integer(), nullable=False)
    houseKey = Column(String(10), nullable=False, unique=True)
    firebaseId = Column(String(100), nullable=False)

    def __init__(self, landlordId):
        self.landlord_id = landlordId
        print(firebase)
        self.firebaseId = firebase.get_firebase_id()
       

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

