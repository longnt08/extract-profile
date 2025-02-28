import hashlib
import datetime
from API.common.ElasticClient import ElasticClient

class CrawlerRepository:
    def __init__(self):
        self.elastic_client = ElasticClient()

    async def insert_raw_html(self, url, content) -> str:
        doc_id = hashlib.md5(url.encode()).hexdigest()
        time_stamp = datetime.datetime.now().isoformat(timespec='seconds').replace("T", " ")
        await self.elastic_client.insert_data("raw_homepages", doc_id, {"url": url, "time_stamp": time_stamp, "html": content})
        
        return doc_id
    
    async def insert_parsed_html(self, raw_id, url, body):
        time_stamp = datetime.datetime.now().isoformat(timespec='seconds').replace("T", " ")
        await self.elastic_client.insert_data("parsed_homepages", raw_id, {"url": url, "time_stamp": time_stamp, "body": body})

    async def get_parsed_html(self, doc_id: str) -> str:
       query = {
          "query": {
              "term": {
                  "_id": doc_id
              } 
          } 
       } 
       parsed_html = await self.elastic_client.search_data(index="parsed_homepages", query=query)
       result = parsed_html["hits"]["hits"][0]["_source"]["body"]
       return result