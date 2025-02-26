import uuid
from API.common.ElasticClient import ElasticClient

class ProcessorRepository:
    def __init__(self):
        self.elastic_client = ElasticClient()
    
    async def save_extracted_info(self, url,doc_id, extracted_data):
        await self.elastic_client.insert_data("processed_experts", doc_id, {"url": url, "value": extracted_data})