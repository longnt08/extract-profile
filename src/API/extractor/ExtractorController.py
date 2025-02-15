from fastapi import APIRouter
from API.extractor.ExtractorService import ExtractorService
from API.extractor.ExtractorRepository import ExtractorRepository

router = APIRouter()
extractor_service = ExtractorService()
extractor_repo = ExtractorRepository()

@router.get("/extract")
async def extract():
    raw_data_list = await extractor_repo.get_raw_html()
    extracted_results = []

    for raw_data in raw_data_list:
        extracted = await extractor_service.parse_html(raw_data["html"])
        await extractor_repo.save_parsed_data(raw_data["id"], raw_data["url"], extracted["title"], extracted["body"])
        extracted_results.append(extracted)

    return extracted_results