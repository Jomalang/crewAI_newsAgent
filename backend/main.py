from YoutubeAgent.agent import NewsAgent, run
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],  # 모든 출처 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.post("/ask")
async def ask_to_agent(body: dict = Body(...)):
    url = body["url"]
    result = run(inputs = {"url": url})
    return {
        "result": result.raw
    }


