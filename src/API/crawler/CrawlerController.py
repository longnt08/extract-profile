from fastapi import APIRouter
from API.crawler.CrawlerService import CrawlerService
from API.crawler.CrawlerRepositoty import CrawlerRepository

router = APIRouter()
crawler_service = CrawlerService()
crawler_repo = CrawlerRepository()

@router.post("/crawl")
async def crawl(url: str):
    content = await crawler_service.fetch_data(url)
    if content:
        doc_id = await crawler_repo.save_raw_html(content["url"], content["content"])
        return {"message": "Data saved successfully", "doc_id": doc_id}
    return {"error": "Failed to fetch data"}