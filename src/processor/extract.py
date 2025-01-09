import os
import requests
from transformers import pipeline
from http.client import responses
from dotenv import load_dotenv
from pyexpat.errors import messages


load_dotenv()

OPEN_API_KEY = os.getenv("OPEN_API_KEY")

# fetch HTML content from a given URL
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None



if __name__ == '__main__':
    html_content = fetch_html("https://math.uchicago.edu/~ngo/")
    prompt = '''Get name, title from this html data and return json format of result: {html_content}'''
