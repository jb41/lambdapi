import aiosqlite
from typing import Dict, \
                   Optional
from fastapi import APIRouter, \
                    Body, \
                    HTTPException, \
                    Request
from fastapi.responses import JSONResponse, \
                              StreamingResponse

from services.database import database_name as db_name
from services.helpers import parse_output
from services.run_code import RunCode



router = APIRouter()



@router.api_route("/{slug}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def run(slug: str, request: Request, body_params: Optional[Dict[str, str]] = Body(None)):
    try:
        async with aiosqlite.connect(db_name) as db:
            cursor = await db.execute("SELECT runtime, code FROM functions WHERE slug=?", (slug,))
            row = await cursor.fetchone()

        if row:
            query_params = dict(request.query_params)
            body_params = body_params if body_params else {}
            params = { **query_params, **body_params }

            runtime_name, code = row[0], row[1]
            stdout, stderr, output_file = RunCode(slug, runtime_name, code).run(params.values())

            if stderr:
                return JSONResponse(content={ "error": stderr.strip() }, status_code=500)
            else:
                if output_file:
                    return StreamingResponse(output_file["content"], media_type=output_file["mime_type"])
                else:
                    return JSONResponse(content=parse_output(stdout.strip()), status_code=200)
            
        else:
            raise HTTPException(status_code=404, detail="Function not found")

    except Exception as excep:
        import sys, traceback
        _, _, tb = sys.exc_info()  # Get the traceback information
        tb_info = traceback.extract_tb(tb)
        filename, line, func, _ = tb_info[-1]  # Extract the file name, line number, and function name from the traceback
        print(f"An exception occurred in {filename}, line {line}, in {func}: {excep}")

        return JSONResponse(content={ "error": str(excep) }, status_code=500)


