import docker, \
       os, \
       random, \
       string, \
       subprocess
from io import BytesIO
import mimetypes
from typing import Tuple

from services.config import config
from services.redis_hostname import redis_hostname



class RunContainerizedCode:
    def __init__(self, image_name: str, compile_cmd: str, execute_cmd: str) -> Tuple[str, str]:
        self._client = docker.from_env()
        self._image_name = image_name
        self._compile_cmd = compile_cmd
        self._execute_cmd = execute_cmd


    def __random_string(self, prefix: str, length: int = 16) -> str:
        return prefix + '-' + ''.join(random.choices(string.ascii_letters, k=length))


    def __outside_file_name(self, container_name: str, file_name: str) -> str:
        file_extension = file_name.split('.')[-1]
        return f"tmp/{container_name}.{file_extension}"


    def __copy_file_outside(self, container, output_file):
        file_name = self.__outside_file_name(container.name, output_file)
        copy_cmd = f"docker cp {container.name}:/app/{output_file} {file_name}"
        subprocess.run(copy_cmd, shell=True, check=True)

        return file_name


    def __system_files(self):
        return [
            'main', 'main.out',
            'node_modules', 'package-lock.json', 'package.json',
            'Gemfile', 'Gemfile.lock',
        ]


    def __get_first_file(self, exec_result):
        if exec_result.exit_code != 0:
            return None

        files = exec_result.output.decode('utf-8').splitlines()
        files = [file for file in files if file not in self.__system_files()]

        if len(files) == 0:
            return None

        files.sort()
        return files[0]


    def __output_file_name(self, container):
        cmd = 'find /app -maxdepth 1 -type f ! -name ".*" -exec basename {} \\;'
        output_file = self.__get_first_file(container.exec_run(cmd=cmd))

        return output_file


    def __read_file_to_memory(self, file_name):
        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"

        with open(file_name, "rb") as file:
            content = file.read()

        return { "content": BytesIO(content), "mime_type": mime_type }


    def __volumes(self):
        return { config['storage_mount_point']: { "bind": "/data", "mode": "rw" } }


    def __env_vars(self):
        envs = {}
        redis_host = redis_hostname()
        if redis_host:
            envs["REDIS_HOST"] = redis_host
        
        return envs


    def run(self, input_file: str, args: list = []):
        container_name = self.__random_string(self._image_name)
        container = self._client.containers.run(self._image_name, name=container_name, detach=True,
                                                volumes=self.__volumes(),
                                                network_mode="host",
                                                environment=self.__env_vars())

        copy_to_docker_cmd = f"docker cp {input_file} {container_name}:/app/main"
        subprocess.run(copy_to_docker_cmd, shell=True, check=True)

        if self._compile_cmd:
            result = container.exec_run(cmd=self._compile_cmd, tty=True, stderr=True)

            if result.exit_code != 0:
                container.kill()
                container.remove()

                return "", result.output.decode("utf-8"), None

        run_cmd = self._execute_cmd + ' ' + ' '.join(args)
        result = container.exec_run(cmd=run_cmd, tty=True, stderr=True)

        output_file_name = self.__output_file_name(container)
        if output_file_name:
            outside_file_name = self.__copy_file_outside(container, output_file_name)
            output_file = self.__read_file_to_memory(outside_file_name)
            os.remove(outside_file_name)
        else:
            output_file = None

        stdout = result.output.decode("utf-8")
        stderr = result.output.decode("utf-8") if result.exit_code != 0 else ""

        container.kill()
        container.remove()

        return stdout, stderr, output_file
