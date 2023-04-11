import os, \
       subprocess

from services.config import runtimes_config as rt_config
from services.create_dockerfile import CreateDockerfile
from services.database import create_table, seed_database
from services.helpers import dockerfiles_dir



# Create functions table
print("Creating functions table...")
create_table()
seed_database()


# Create tmp directory
print("Creating tmp directory...")
if not os.path.exists("tmp"):
    os.makedirs("tmp")


# Create Dockerfiles and build all images
print("Creating dockerfiles and building images...")
if not os.path.exists(dockerfiles_dir):
    os.makedirs(dockerfiles_dir)


for runtime_name, runtime_config in rt_config.items():
    print("Building image for: " + runtime_config['name'])
    create_dockerfile = CreateDockerfile(runtime_name, runtime_config)
    create_dockerfile()

    command = f"docker build -t {runtime_config['image_name']} -f {dockerfiles_dir}/{runtime_name}.Dockerfile ."
    subprocess.run(command, shell=True, check=True)
