from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from typing import Dict, List

from services.llm.openai import OpenAi
from services.helpers import extract_code_and_text



router = APIRouter()


@router.post("")
async def get_completions(messages: List[Dict] = Body(...), language: str = Body(...)):
    message = OpenAi.chat_completion(messages, language)
    splitted_response_data = extract_code_and_text(message['content'])
    response_data = { **splitted_response_data, 'message': message }

    return JSONResponse(content=response_data, status_code=200)
