from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn

from api.runs import router as runs_router
from api.functions import router as functions_router
from api.runtimes import router as runtimes_router
from api.completions import router as completions_router



app = FastAPI()
app.include_router(runs_router, prefix="/run")
app.include_router(functions_router, prefix="/api/functions")
app.include_router(runtimes_router, prefix="/api/runtimes")
app.include_router(completions_router, prefix="/api/completions")
app.mount("/", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
