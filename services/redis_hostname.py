import docker

from services.config import config



def get_redis_container():
    client = docker.from_env()
    for container in client.containers.list():
        if container.name == 'redis':
            return container
    return None


def get_redis_ip_address(container):
    for network in container.attrs["NetworkSettings"]["Networks"].values():
        if network["IPAddress"]:
            return network["IPAddress"]
    return None


def redis_hostname():
    redis_host = config.get("redis_host")

    if redis_host:
        return redis_host

    redis_container = get_redis_container()
    if redis_container:
        return get_redis_ip_address(redis_container)

    return None
