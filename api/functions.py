import aiosqlite, \
       json

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from services.helpers import generate_unique_slug, \
                             endpoint_url
from services.database import database_name as db_name



router = APIRouter()


@router.get("")
async def get_functions():
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("SELECT * FROM functions ORDER BY name ASC, created_at DESC")
        rows = await cursor.fetchall()
    return [
        {
            "id": r[0], "name": r[1], "runtime": r[3], "created_at": r[5], "endpoint_url": endpoint_url(r[2])
        } for r in rows
    ]


@router.get("/{function_id}")
async def get_function(function_id: int):
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("SELECT * FROM functions WHERE id=?", (function_id,))
        row = await cursor.fetchone()

    if row:
        return {
            "id": row[0], "name": row[1], "runtime": row[3], "code": row[4], "endpoint_url": endpoint_url(row[2])
        }
    else:
        raise HTTPException(status_code=404, detail="Function not found")


@router.post("", status_code=201)
async def create_function():
    slug = await generate_unique_slug()
    if not slug:
        raise HTTPException(status_code=500, detail="Failed to generate a unique slug")

    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("INSERT INTO functions (slug, name, created_at) VALUES (?, ?, datetime('now'))", (slug, "Unnamed Function"))
        await db.commit()



    return JSONResponse(content={ "id": cursor.lastrowid, "slug": slug }, status_code=201)


@router.put("/{function_id}")
async def update_function(function_id: int, request: Request):
    try:
        function_data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    async with aiosqlite.connect(db_name) as db:
        set_clauses = []
        values = []

        if 'name' in function_data and function_data['name'] is not None:
            set_clauses.append("name=?")
            values.append(function_data['name'])
        if 'runtime' in function_data and function_data['runtime'] is not None:
            set_clauses.append("runtime=?")
            values.append(function_data['runtime'])
        if 'code' in function_data and function_data['code'] is not None:
            set_clauses.append("code=?")
            values.append(function_data['code'])

        if not set_clauses:
            raise HTTPException(status_code=400, detail="No fields to update")

        values.append(function_id)
        await db.execute("UPDATE functions SET " + ', '.join(set_clauses) + " WHERE id=?", tuple(values))
        await db.commit()

    return await get_function(function_id)


@router.delete("/{function_id}")
async def delete_function(function_id: int):
    async with aiosqlite.connect(db_name) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM functions WHERE id=?", (function_id,))
        count = await cursor.fetchone()

        if count[0] == 0:
            raise HTTPException(status_code=404, detail=f"Function with ID {function_id} not found")

        await db.execute("DELETE FROM functions WHERE id=?", (function_id,))
        await db.commit()

    return Response(status_code=204)
