import ast, \
       os, \
       random, \
       re, \
       string, \
       yaml
from typing import Any, Optional

from services.config import config



dockerfiles_dir = 'dockerfiles'


def parse_output(data: str) -> Any:
    try:
        parsed_data = ast.literal_eval(data)
        if isinstance(parsed_data, dict):
            return parsed_data
        else:
            return str(parsed_data)
    except (ValueError, SyntaxError):
        return data


def get_openai_config() -> dict[str, Any]:
    return config.get('llm', {}).get('openai', {})


def openai_apikey() -> str:
    return get_openai_config().get('apikey')


def openai_system_prompt(language) -> str:
    return get_openai_config().get('system_prompt').format(language=language)


def openai_model_params() -> dict[str, Any]:
    return get_openai_config().get('model_params', { 'model': 'gpt-3.5-turbo', 'temperature': 0.4, 'top_p': 1 })


# TODO
# Change to https
def endpoint_url(slug: str) -> str:
    return f"http://{config.get('hostname')}/run/{slug}"


# TODO: Add a check to make sure the slug is unique
async def generate_unique_slug(length: int = 16) -> Optional[str]:
    characters = string.ascii_lowercase + string.digits
    slug = ''.join(random.choices(characters, k=length))

    return slug


def extract_code_and_text(input_str):
    code_regex = re.compile(r"```([\s\S]*?)```", re.MULTILINE)
    code_blocks = []
    text_blocks = []
    last_index = 0

    for match in code_regex.finditer(input_str):
        code_block = match.group(1).strip()
        if re.match(r'^\w+\n', code_block):
            code_block = re.sub(r'^\w+\n', '', code_block)
        code_blocks.append(code_block)
        text_blocks.append(input_str[last_index:match.start()].strip())
        last_index = match.end()

    text_blocks.append(input_str[last_index:].strip())

    return {
        'code': '\n'.join(code_blocks),
        'text': '\n'.join(text_blocks)
    }
