from fastapi import APIRouter
from fastapi.responses import JSONResponse
from common.ElasticClient import ElasticClient
from API.processor.processor_service import ProcessorService
from API.processor.processor_repository import ProcessorRepository

router = APIRouter()
processor_service = ProcessorService()
processor_repository = ProcessorRepository()
es = ElasticClient()

@router.post("/process")
async def process(url: str):
    try:
        parsed_html = await es.search_data("parsed_homepages", url)

        # neu da co, trich xuat thong tin
        if parsed_html["hits"]["total"]["value"] > 0:
            parsed_data = parsed_html["hits"]["hits"][0]["_source"]["body"]
            extracted_data = await processor_service.extract_profile(parsed_data)

            # luu thong tin da extract vao index 
            doc_id = await processor_repository.save_extracted_info(url, extracted_data)

            return JSONResponse(status_code=200, content={"extracted_homepages": extracted_data, "id": doc_id})
        else:
            return JSONResponse(status_code=404, content="This homepage have not been crawled yet.")
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))