from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from API.common.ElasticClient import ElasticClient
from API.processor.processor_service import ProcessorService
from API.processor.processor_repository import ProcessorRepository

router = APIRouter()
processor_service = ProcessorService()
processor_repository = ProcessorRepository()
es = ElasticClient()

# extract HTML data
@router.post("/process/{id}")
async def process(id: str):
    try:
        query = {
                "query": {
                    "term": {
                        "_id": id
                    }
                }
            }
        parsed_html = await es.search_data(index="parsed_homepages", query=query)

        # neu da co, trich xuat thong tin
        if parsed_html["hits"]["total"]["value"] > 0:
            parsed_data = parsed_html["hits"]["hits"][0]["_source"]["body"]
            url = parsed_html["hits"]["hits"][0]["_source"]["url"] 
            extracted_data = await processor_service.extract_profile(parsed_data)

            # luu thong tin da extract vao index 

            await processor_repository.insert_extracted_info(url, id, extracted_data)

            return JSONResponse(status_code=200, content=extracted_data)
        else:
            return JSONResponse(status_code=404, content="This homepage have not been crawled yet.")
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))

# get extracted info
@router.get("/get_extracted_expert/{id}")
async def get_extracted_expert(id: str):
    try:
        result = await processor_repository.get_extracted_info(id)

        if not result:
            raise HTTPException(status_code=404, detail="Content not found") 
        
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})