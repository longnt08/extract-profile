import requests
import torch
from itertools import groupby
from bs4 import BeautifulSoup
from transformers import pipeline
from http.client import responses
from pyexpat.errors import messages

# fetch HTML content from a given URL
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.text

        # soup = BeautifulSoup(response.content, "html.parser")
        # html_content = soup.prettify()
        # return html_content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

# aggregate output
def aggregate_entities(results):
    entities = []
    for _, group in groupby(results, lambda x: x['entity'].split('-')[1]):
        group = list(group)
        entity = {
            "entity": group[0]['entity'].split('-')[1],
            "score": sum(item['score'] for item in group) / len(group),
            "word": " ".join(item['word'] for item in group),
            "start": group[0]['start'],
            "end": group[-1]['end']
        }
        entities.append(entity)
    return entities

if __name__ == '__main__':
    url = [
        "https://math.uchicago.edu/~ngo/",
        "https://vuhavan.com/profile/",
    ]
    html_content = fetch_html(url[1])
    # print(html_content)

    device = 0 if torch.cuda.is_available() else -1

    pipe = pipeline("token-classification", model="autoevaluate/entity-extraction", device=device)

    result = pipe(html_content)
    print(result)

    # aggregated_result = aggregate_entities(result)

    # print(aggregated_result)