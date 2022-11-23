from firebase_admin import credentials, storage
import firebase_admin, base64
from firebase_admin import firestore
import datetime

class Firebase:


    def __init__(self):  
        self._serviceAccountPath = r'./static/ServiceAccount.json'
    

    def setServiceAccountPath(self, path):
        self._serviceAccountPath = path

    def init_app(self):
        cred = credentials.Certificate(self._serviceAccountPath)
        try:
            app = firebase_admin.get_app()
        except ValueError as e:
            cred = credentials.Certificate(self._serviceAccountPath)
            firebase_admin.initialize_app(cred, {'storageBucket' : 'roomr-222721.appspot.com'})
        self._db = firestore.client()

    def create_blob_no_cache(self, filePath):
        bucket = storage.bucket()
        blob = bucket.blob(filePath)
        blob.cache_control = "no-cache"
        return blob

    def get_firebase_id(self):
        db = self._db
        collection = db.collection(u'House')
        document = collection.document()
        document.set({})
        return document.id

    def delete_document(self, firebaseId):
        db = self._db
        collection = db.collection(u'House')
        document = collection.document(firebaseId)
        document.delete()
        
    def tenant_account_created_notification(self, firebaseId, tenantData): 
        landlordCollection = self._db.collection(u'House').document(firebaseId).collection("Landlord")
        content = {
            "Name": "TenantAccountCreated",
            "houseKey": tenantData["houseKey"],
            "dateCreated": datetime.datetime.now(),
            "data": {
                "firstName": tenantData["firstName"],
                "lastName": tenantData["lastName"],
                "email": tenantData["email"]
            }
        }
        landlordCollection.document().set(content)
        

       



