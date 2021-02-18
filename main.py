import configparser
import sys, os

from fastapi import FastAPI
from google.cloud import firestore
# from google.oauth2 import service_account

sys.path.append(os.getcwd())

app = FastAPI()

config = configparser.ConfigParser()
config.read('config.ini')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["FIRESTORE"]["ServiceAccountPath"]
# service_account_path = config["FIRESTORE"]["ServiceAccountPath"]
# credentials = service_account.Credentials.from_service_account_file(service_account_path)

db = firestore.Client()
collection_ref = db.collection(u'insurance-risk')
@app.get("/")
async def root():
    return {"message": "Hello World"}
    

@app.get("/risk/{id}")
async def get_risk(id: int=1):

    query = collection_ref.where("Id", "==", int(id))
    docs = query.get()
    l = []
    for doc in docs:
        l.append(doc.to_dict())

    response = {
        "data": l
    }
    return response