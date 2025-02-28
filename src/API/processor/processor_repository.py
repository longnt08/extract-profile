import uuid
from API.common.ElasticClient import ElasticClient

class ProcessorRepository:
    def __init__(self):
        self.elastic_client = ElasticClient()
    
    async def insert_extracted_info(self, url, doc_id, extracted_data):
        await self.elastic_client.insert_data("processed_experts", doc_id, {"url": url, "value": extracted_data})

    async def get_extracted_info(self, id):
        query = {
            "query": {
                "term": {
                    "_id": id
                }
            }
        }
        result = await self.elastic_client.search_data(index="processed_experts", query=query)
        extracted_expert = result["hits"]["hits"][0]["_source"]
        return extracted_expert