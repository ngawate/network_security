import os
import sys
import certifi

ca = certifi.where()
from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd
import numpy as np

from networksecurity.utils.main_utils.utils import load_object

from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_COLLECTION_NAME

client = pymongo.MongoClient(mongo_db_url)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

templates = Jinja2Templates(directory="./templates")

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is sucessful")
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e, sys)
    
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor, final_model)

        print(df.iloc[0])

        y_pred = network_model.predict(df)
        print(y_pred)
        
        df['Predicted_Column'] = y_pred

        df.to_csv("prediction_output/output.csv")

        table_html = df.to_html(classes='table table-striped')

        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
     
    except Exception as e:
        logging.error(e)
        raise NetworkSecurityException(e, sys)
    
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
