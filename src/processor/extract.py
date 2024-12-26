from http.client import responses

import requests
import openai
import os
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

def send_to_chatgpt(html_content, prompt):
    openai.api_key = OPEN_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant skilled at processing HTML data."},
                {"role": "user", "content": f"HTML content: \n{html_content}"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with chatgpt: {e}")
        return None

if __name__ == '__main__':
    html_content = fetch_html("https://math.uchicago.edu/~ngo/")
    prompt = "Get name, title from this html data and return json format of result"

    result = send_to_chatgpt(html_content, prompt)