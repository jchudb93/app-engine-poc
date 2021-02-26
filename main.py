import configparser
import sys, os
import pickle
import os.path

from os import path

from fastapi import FastAPI
from pydantic import BaseModel

from google.cloud import firestore
from google.cloud import storage
from io import BytesIO

sys.path.append(os.getcwd())



config = configparser.ConfigParser()
config.read('config.ini')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config["GCP"]["ServiceAccountPath"]

if not path.exists('./model.pkl'):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('data-poc-gcp')
    blob = bucket.blob('models/model.pkl')
    blob.download_to_filename('./model.pkl')
model = pickle.load(open('./model.pkl', 'rb'))

db = firestore.Client()
collection_ref = db.collection(u'insurance-risk')
sales_ref = db.collection('sales')

app = FastAPI()

def convert_to_int(word):
    word_dict = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8,
                'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'zero':0, 0: 0}
    return word_dict[word]

class Sale (BaseModel):
    id: str

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

@app.post("/sales/")
async def predict(sale: Sale):

    
    query = sales_ref.where("id", "==", int(sale.id))
    docs = query.get()
    l = []
    for doc in docs:
        l.append(doc.to_dict())

    prediction = []
    arr = []
    if len(l) > 0:
        
        sale = l[0]
        arr.append(convert_to_int(sale["rate"] if sale["rate"] != '' else 0))
        arr.append(sale["sales_in_first_month"])
        arr.append(sale["sales_in_second_month"])
        prediction = model.predict([arr])
        response = {
            "data": l,
            "prediction": prediction[0] if prediction[0] else 0 
        }

        return response

    response = {
        "status": 206,
        "message": "Empty"
    }

    return response