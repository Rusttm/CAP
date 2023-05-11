from API_Docker.ConnDocker.ConnDCMainClass import ConnDCMainClass
import docker
class ConnDCTest(ConnDCMainClass):
    """ from https://docker-py.readthedocs.io/en/stable/client.html"""
    client = None
    def __init__(self):
        super().__init__()
        self.client = docker.from_env()

    def get_cont_list(self):
        return self.client.containers.list()


if __name__ == '__main__':
    connector = ConnDCTest()
    print(connector.get_cont_list())