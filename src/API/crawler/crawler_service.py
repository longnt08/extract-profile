import requests
from bs4 import BeautifulSoup

class CrawlerService:
    async def fetch_data(self, url: str) :
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.text
            else:
                return None
        except Exception as e:
            print(f"Error when get data: {e}")
            return None
        
    async def parse_html(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        body = " ".join(soup.get_text().split())
        return body