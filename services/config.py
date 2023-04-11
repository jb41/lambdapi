import os, \
       yaml
from typing import Any



def get_config(filename) -> dict[str, Any]:
    with open(filename) as file:
        return yaml.safe_load(file)


def load_yaml_files(directory: str) -> dict[str, Any]:
    yaml_files = {}
    for filename in os.listdir(directory):
        if filename.endswith('.yaml') or filename.endswith('.yml'):
            with open(os.path.join(directory, filename)) as file:
                yaml_data = yaml.safe_load(file)
                key = filename.rsplit('.', 1)[0]
                yaml_files[key] = yaml_data

    return yaml_files


config = get_config("config.yaml")
runtimes_config = load_yaml_files("runtimes")
