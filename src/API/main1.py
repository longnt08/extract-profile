from fastapi import FastAPI
from API.crawler.CrawlerController import router as crawler_router
from API.extractor.ExtractorController import router as extractor_router

app = FastAPI()

app.include_router(crawler_router, prefix="/crawler", tags=["Crawling"])
app.include_router(extractor_router, prefix="/extractor", tags=["Extraction"])

@app.get("/")
async def root():
    return {"message": "Welcome to Extract System"}

