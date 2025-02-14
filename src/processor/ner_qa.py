import requests
from transformers import pipeline

# load NER model
ner_model = pipeline("ner", grouped_entities=True)

# load QA model
qa_model = pipeline("question-answering")

# ham lay du lieu html
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching url: {e}")
        return None

if __name__ == '__main__':
    url = "https://vuhavan.com/profile/"
    text = fetch_html(url)

    # uer NER to extract named entities
    entities = ner_model(text)

    # display identified entities
    for entity in entities:
        print(f"Entity: {entity['word']}, Type: {entity['entity_group']}, Score: {entity['score']:.2f}")
    
    # define questions and context
    questions = [
        "What is the name of the person in the profile?",
        "Where does the person currently live?",
        "What is the profession of the person?",
        "Which university did the person graduate from?"
    ]

    # get answer for each question
    for question in questions:
        answer = qa_model(question=question, context=text)
        print(f"Q: {question}")
        print(f"A: {answer['answer']} (Score: {answer['score']:.2f})\n")