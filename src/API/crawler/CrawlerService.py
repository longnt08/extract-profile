import requests

class CrawlerService:
    async def fetch_data(self, url: str) -> dict:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return {"url": url, "content": response.text}
            else:
                return None
        except Exception as e:
            print(f"Error when get data: {e}")
            return None