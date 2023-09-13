from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"Opt_expert": "Hello!"}
