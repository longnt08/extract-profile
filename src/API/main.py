import uvicorn
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from processor.test import process_profile
from pydantic import BaseModel

app = FastAPI()

class ProfileRequest(BaseModel):
    url: str
    fields: list[str]

@app.post('/entity-extraction/get-json-info')
async def get_json_info(request: ProfileRequest):
    try:
        response = requests.get(request.url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {e}")
    
    profile_text = response.text
    extracted_data = process_profile(profile_text, fields=request.fields)

    return JSONResponse(status_code=200, content=extracted_data)

if __name__ == '__main__':
    uvicorn.run(app)