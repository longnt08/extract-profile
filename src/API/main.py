import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from API.crawler.crawler_controller import router as crawler_router
from API.processor.processor_controller import router as processor_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(crawler_router, prefix="/experts", tags=["Crawling"])
app.include_router(processor_router, prefix="/experts", tags=["Processing"])

@app.get("/")
async def root():
    return {"message": "Welcome to Extract System"}

if __name__ == '__main__':
    uvicorn.run(app)