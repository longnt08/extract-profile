from fastapi import APIRouter
from API.crawler.crawler_service import CrawlerService
from API.crawler.crawler_repository import CrawlerRepository

router = APIRouter()
crawler_service = CrawlerService()
crawler_repo = CrawlerRepository()

@router.post("/crawl")
async def crawl(url: str):
    content = await crawler_service.fetch_data(url)
    parsed_html = await crawler_service.parse_html(content)
    if content:
        doc_id = await crawler_repo.save_raw_html(url, content)
        await crawler_repo.save_parsed_html(doc_id, url, parsed_html)

        return {"message": "Data saved successfully", "doc_id": doc_id}
    return {"error": "Failed to fetch data"}