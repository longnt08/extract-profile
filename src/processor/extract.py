import os
import requests
import torch
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

    # result = classifier("I love hugging face models")
    # print(result)

    device = 0 if torch.cuda.is_available() else -1
    classifier = pipeline('sentiment-analysis', device=device)

    texts = [
        "I love this product. It's absolutely amazing",
        "This is the worst experience I've ever had"
    ]

    results = classifier(texts)

    for text, result in zip(texts, results):
        print(f"Text: {text}")
        print(f"Sentiment: {result['label']}, Score: {result['score']:.4f}")