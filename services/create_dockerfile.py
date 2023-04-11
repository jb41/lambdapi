class CreateDockerfile:
    def __init__(self, runtime_name: str, runtime_config: str):
        self.runtime_config = runtime_config
        self.dockerfile_filename = self.__dockerfile_full_name(runtime_name)


    def __call__(self):
        dockerfile = self.__dockerfile_template().format(
            repository_image_name=self.runtime_config["docker"]["repository_image"],
            docker_run_cmd=self.runtime_config["docker"]["run_cmd"],
        )

        with open(self.dockerfile_filename, "w") as f:
            f.write(dockerfile)


    def __dockerfile_template(self):
        return """\
FROM {repository_image_name}
WORKDIR /app
RUN {docker_run_cmd}
VOLUME ["/data"]
CMD ["sh", "-c", "while true; do sleep 10; done"]
"""


    def __dockerfile_full_name(self, filename: str):
        return "dockerfiles/" + filename + ".Dockerfile"
