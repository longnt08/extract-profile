from bs4 import BeautifulSoup

class ExtractorService:
    async def parse_html(self, html_content: str):
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.title.string if soup.title else "No title"
        body = soup.get_text()
        return {"title": title, "body": body}