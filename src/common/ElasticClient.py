from elasticsearch import AsyncElasticsearch

class ElasticClient:
    def __init__(self):
        self.es = AsyncElasticsearch(hosts=["http://localhost:9200"])
    
    async def insert_data(self, index, doc_id, data):
        await self.es.index(index=index, id=doc_id, document=data)

    async def search_data(self, index, query):
        return await self.es.search(
            index=index,
            body=query
        )
    
    async def close(self):
        await self.es.close()