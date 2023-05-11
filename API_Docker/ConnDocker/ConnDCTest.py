from API_Docker.ConnDocker.ConnDCMainClass import ConnDCMainClass
import docker
class ConnDCTest(ConnDCMainClass):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ConnDCTest()
    # connector.get_invin_filtered_by_date(from_date="2023-01-01", to_date="2023-02-01", to_file=True)