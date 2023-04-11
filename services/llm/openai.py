import openai
from typing import List

from services.helpers import openai_apikey, \
                             openai_system_prompt, \
                             openai_model_params



openai.api_key = openai_apikey()
model_params = openai_model_params()

class OpenAi:
    @staticmethod
    def chat_completion(messages: List[dict], language: str) -> dict:
        completion = openai.ChatCompletion.create(
            model=model_params['model'],
            temperature=model_params['temperature'],
            top_p=model_params['top_p'],
            messages=OpenAi._messages_with_prompt(messages, language)
        )
        return completion.choices[0].message


    @staticmethod
    def _messages_with_prompt(messages: List[str], language) -> List[dict]:
        return [{ "role": "system", "content": openai_system_prompt(language) }] + messages
