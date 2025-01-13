import json
import requests
import torch
from transformers import pipeline
from bs4 import BeautifulSoup

device = 0 if torch.cuda.is_available() else -1
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True, device=device)
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
    
# ham lay ten
def extract_name(text):
    entities = ner_pipeline(text)
    for entity in entities:
        if entity["entity_group"] == "PER":
            return entity["word"]
    return None

# ham trich xuat thong tin bang QA
def extract_info(question, context):
    result = qa_pipeline(question=question, context=context)
    return result["answer"]

# main processor
def process_profile(text, fields=None):
    """
    Trích xuất thông tin từ hồ sơ dựa trên các trường yêu cầu.
    :param text: Văn bản hồ sơ cần xử lý.
    :param fields: Danh sách các trường cần trích xuất (ví dụ: ["name", "age"]). 
    Nếu None, sẽ trích xuất tất cả các trường.
    :return: Chuỗi JSON chứa thông tin được yêu cầu.
    """

    # Danh sach cac truong trich xuat voi ham tuong ung

    extractors = {
        "name": lambda text: extract_name(text),
        "age": lambda text: extract_info("What is the age?", text),
        "address": lambda text: extract_info("What is the address?", text),
        "email": lambda text: extract_info("What is the email?", text),
        "professions": lambda text: extract_info("What is the professions?", text),
        "organizations": lambda text: extract_info("What is the organizations?", text),
    }

    # neu fields None, mac dinh lay tat ca cac truong
    if fields is None:
        fields = extractors.keys()

    # trich xuat chi cac truong duoc yeu cau
    result = {}
    for field in fields:
        if field in extractors:
            result[field] = extractors[field](text)
        else:
            result[field] = None # tra ve None neu truong khong hop le

    return json.dumps(result, indent=4)
    
if __name__ == '__main__':
    html_content = fetch_html("https://en.wikipedia.org/wiki/Stephen_Hawking")

    soup = BeautifulSoup(html_content, "html.parser")

    text = soup.getText()

    output_json = process_profile(text)
    print(output_json)

    del ner_pipeline
    del qa_pipeline
    del output_json

    torch.cuda.empty_cache()