import hashlib
import datetime
from API.common.ElasticClient import ElasticClient

class CrawlerRepository:
    def __init__(self):
        self.elastic_client = ElasticClient()

    async def save_raw_html(self, url, content):
        doc_id = hashlib.md5(url.encode()).hexdigest()
        time_stamp = datetime.datetime.now().isoformat(timespec='seconds').replace("T", " ")
        await self.elastic_client.insert_data("raw_homepages", doc_id, {"url": url, "time_stamp": time_stamp, "html": content})
        
        return doc_id
    
    async def save_parsed_html(self, raw_id, url, body):
        time_stamp = datetime.datetime.now().isoformat(timespec='seconds').replace("T", " ")
        await self.elastic_client.insert_data("parsed_homepages", raw_id, {"url": url, "time_stamp": time_stamp, "body": body})