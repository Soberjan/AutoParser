import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.responses import RedirectResponse
import uvicorn

from examples.w9.routes.resume.main import router as resume_router
from examples.w9.routes.t1.main import router as t1_router



APP_NAME = "IT2GO Python Flow"
VERSION = "0.0.2"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Service started!")

    yield

    print("Service finished!")

app = FastAPI(title=APP_NAME, version=VERSION, lifespan=lifespan)

@app.get("/")
def main_function():
    return RedirectResponse(url="/docs")

app.include_router(resume_router)
app.include_router(t1_router)

if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(
        "run:app", 
        host="0.0.0.0",
        port=5000,
        workers=int(os.getenv("WORKERS_COUNT", 1))
        )