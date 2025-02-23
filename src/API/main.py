import uvicorn
from typing import List
from fastapi import FastAPI, Query
from common.ElasticClient import ElasticClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from API.crawler.crawler_controller import router as crawler_router
from API.processor.processor_controller import router as processor_router
import json

app = FastAPI()
es = ElasticClient()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Extract System"}

app.include_router(crawler_router, prefix="/experts", tags=["Crawling"])
app.include_router(processor_router, prefix="/experts", tags=["Processing"])

# chuc nang search
@app.get("/experts/search", tags=['Searching'])
async def search(url: str, fields: List[str]=Query(...)):
    try:
        query = {
            "query": {
                "term": {
                    "url": url
                }
            }
        }
        print(query)
        extracted_data = await es.search_data(index="processed_experts", query=query)
        if extracted_data["hits"]["total"]["value"] > 0:
            extracted_info = extracted_data["hits"]["hits"][0]["_source"]["value"]

            # luu ket qua
            result = {}
            for field in fields:
                result[field] = extracted_info[field]
            
            return JSONResponse(status_code=200, content=result)
        
        else:
            return JSONResponse(status_code=404, content={"message":"This homepage have not been processed yet."})
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

if __name__ == '__main__':
    uvicorn.run(app)