import os, \
       random, \
       string
from typing import Tuple

from services.config import runtimes_config as rt_config
from services.run_containerized_code import RunContainerizedCode



class RunCode:
    def __init__(self, slug: str, runtime_name: str, code: str) -> Tuple[str, str]:
        self._slug = slug
        self._runtime_name = runtime_name
        self._code = code


    def run(self, args: list):
        try:
            runtime_config = rt_config[self._runtime_name]

            if runtime_config:
                filename = self._slug + ''.join(random.choices(string.ascii_letters, k=16))
                input_file = os.path.join("tmp", filename)

                with open(input_file, "w") as f:
                    f.write(self._code)

                stdout, stderr, output_file = RunContainerizedCode(image_name=runtime_config['image_name'],
                                                                compile_cmd=runtime_config['run'].get('compile'),
                                                                execute_cmd=runtime_config['run'].get('execute')
                                                                ).run(input_file, args)

                return stdout, stderr, output_file

            else:
                raise Exception("Runtime not found")
        
        finally:
            os.remove(input_file)
