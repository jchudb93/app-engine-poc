import configparser

from fastapi import FastAPI

app = FastAPI()

config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())

@app.get("/")
async def root():
    return {"message": "Hello World"}