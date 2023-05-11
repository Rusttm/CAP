from API_Docker.ConnDocker.ConnDCMainClass import ConnDCMainClass
import docker
from python_on_whales import docker as docker2
from python_on_whales import DockerClient
class ConnDCTest(ConnDCMainClass):
    """ from https://docker-py.readthedocs.io/en/stable/client.html"""
    client = None
    docker_compose = None
    def __init__(self):
        super().__init__()
        # self.client = docker.from_env()
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.docker_compose = DockerClient(compose_files=["../Dockerfiles/Pgsql/docker-compose.yml"])

    def get_cont_list(self):
        return self.client.containers.list()

    def up_docker_compose(self):
        # docker_compose = DockerClient(compose_files=["../Dockerfiles/Pgsql/docker-compose.yml"])
        self.docker_compose.compose.up()
    def build_docker_compose(self):
        # docker_compose = DockerClient(compose_files=["../Dockerfiles/Pgsql/docker-compose.yml"])
        self.docker_compose.compose.build()



if __name__ == '__main__':
    connector = ConnDCTest()
    print(connector.get_cont_list())
    print(connector.build_docker_compose())
    print(connector.up_docker_compose())