import uuid
from common.ElasticClient import ElasticClient

class CrawlerRepository:
    def __init__(self):
        self.elastic_client = ElasticClient()

    async def save_raw_html(self, url, content):
        doc_id = str(uuid.uuid4())
        await self.elastic_client.insert_data("raw_homepages", doc_id, {"url": url, "html": content})
        
        return doc_id
    
    async def save_parsed_html(self, raw_id, url, body):
        await self.elastic_client.insert_data("parsed_homepages", raw_id, {"url": url,  "body": body})