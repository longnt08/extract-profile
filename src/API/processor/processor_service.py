import json
from extract_model.ner_and_qa import process_profile

class ProcessorService:
    async def extract_profile(self, parsed_html: str) -> json:
        extracted_data = process_profile(parsed_html)
        result = json.loads(extracted_data)

        return result