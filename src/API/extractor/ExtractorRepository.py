from common.ElasticClient import ElasticClient

class ExtractorRepository:
    def __init__(self):
        self.elastic_client = ElasticClient()

    async def get_raw_html(self):
        query = {"match_all": {}}
        result = await self.elastic_client.search_data("web_raw", query)
        return [{"id": hit["_id"], "url": hit["_source"]["url"], "html": hit["_source"]["html"]} for hit in result["hits"]["hits"]]
    
    async def save_parsed_data(self, raw_id, url, title, body):
        await self.elastic_client.insert_data("web_parsed", raw_id, {"url": url, "title": title, "body": body})