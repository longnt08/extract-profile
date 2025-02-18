import uuid
import requests
from typing import List
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from common.ElasticClient import ElasticClient
from processor.ner_and_qa import process_profile
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from API.crawler.crawler_controller import router as crawler_router

app = FastAPI()

es = ElasticClient()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crawler_router, prefix="/crawler", tags=["Crawling"])

@app.get("/")
async def root():
    return {"message": "Welcome to Extract System"}

@app.get("/entity_extract")
async def  entity_extract(url: str, fields: List[str] = Query(...)):
    try:
        # kiem tra url da co trong Elasticsearch chua
        query = {"query": {"match": {"url": url}}}
        parsed_result = es.search(index="web_parsed", body=query)

        # neu da co, trich xuat thong tin
        if parsed_result["hits"]["total"]["value"] > 0:
            parsed_html = parsed_html = parsed_result["hits"]["hits"][0]["_source"]["body"]
            extracted_data = process_profile(parsed_html, fields=fields)

            return JSONResponse(status_code=200, content=extracted_data)
        else:
            response = requests.get(url)
            if response.status_code != 200:
                return {"error": "Khong the truy cap URL"}
            
            raw_html = response.text

            # parse HTML
            soup = BeautifulSoup(raw_html, "html.parser")
            title = soup.title.string if soup.title else "No title"
            parsed_data = soup.get_text(separator="\n", strip=True)



            # extract thong tin
            extracted_data = process_profile(parsed_data, fields=fields)

            # luu vao Elasticsearch
            doc_id = str(uuid.uuid4())
            es.insert_data("web_raw", doc_id, {"url": url, "html": raw_html})
            es.insert_data(doc_id, url, title, parsed_data)

            return JSONResponse(status_code=200, content=extracted_data)
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))