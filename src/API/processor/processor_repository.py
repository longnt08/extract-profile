import uuid
from common.ElasticClient import ElasticClient

class ProcessorRepository:
    def __init__(self):
        self.elastic_client = ElasticClient()
    
    async def save_extracted_info(self, url, extracted_data):
        doc_id = str(uuid.uuid4())
        await self.elastic_client.insert_data("processed_experts", doc_id, {"url": url, "value": extracted_data})

        return doc_id