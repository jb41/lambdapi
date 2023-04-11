from fastapi import APIRouter
from fastapi.responses import JSONResponse

from services.config import runtimes_config



router = APIRouter()


@router.get("/available")
async def get_available_runtimes():
    available_runtimes = []
    for k, v in runtimes_config.items():
        available_runtimes.append({
            'name': v['name'],
            'runtime': k,
            'monaco_editor_id': v['monaco_editor_id']
        })
    available_runtimes = sorted(available_runtimes, key=lambda x: x['name'])

    return JSONResponse(content=available_runtimes, status_code=200)
