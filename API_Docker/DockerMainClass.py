from Main.CAPMainClass import CAPMainClass


class DockerMainClass(CAPMainClass):
    logger_name = "Docker"

    def __init__(self):
        super().__init__()