import uvicorn
import requests
from typing import List
from pydantic import BaseModel
from elasticsearch import Elasticsearch
from fastapi.responses import JSONResponse
from processor.ner_and_qa import process_profile
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# connect to elasticsearch
es = Elasticsearch(['http://localhost:9200'])

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProfileRequest(BaseModel):
    url: str
    fields: list[str]

@app.get('/getProfileData')
async def getProfileData():
    if es.ping():
        return {"status": "Connected to Elasticsearch"}
    else:
        raise HTTPException(status_code=500, detail="Cannot connect to Elasticsearch")

@app.get('/entityExtraction')
async def entityExtraction(url: str, fields: List[str] = Query(...)):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {e}")
    
    profile_text = response.text
    extracted_data = process_profile(profile_text, fields=fields)

    return JSONResponse(status_code=200, content=extracted_data)


if __name__ == '__main__':
    uvicorn.run(app)