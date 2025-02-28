from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from API.crawler.crawler_service import CrawlerService
from API.crawler.crawler_repository import CrawlerRepository

router = APIRouter()
crawler_service = CrawlerService()
crawler_repo = CrawlerRepository()

# crawl raw & parsed HTML
@router.post("/crawl")
async def crawl(url: str):
    try:
        content = await crawler_service.fetch_data(url)
        parsed_html = await crawler_service.parse_html(content)
        if not content:
            raise HTTPException(status_code=404, detail="Can't get HTML data from this URL")

        doc_id = await crawler_repo.insert_raw_html(url, content)
        await crawler_repo.insert_parsed_html(doc_id, url, parsed_html)

        return JSONResponse(status_code=200, content={"_id": doc_id})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# get parsed HTML    
@router.get("/get_parsed_homepage/{id}")
async def get_parsed_homepage(id: str):
    try:
        result = await crawler_repo.get_parsed_html(doc_id=id)
        if not result:
            raise HTTPException(status_code=404, detail="Content not found")

        return JSONResponse(status_code=200, content={"body": result})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})