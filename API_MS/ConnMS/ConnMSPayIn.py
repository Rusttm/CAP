from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSPayIn(ConnMSMainClass):
    """class to connect payments out"""

    def __init__(self):
        super().__init__()
        self.logger.debug("module ConnMSPayIn started")


if __name__ == '__main__':
    connector = ConnMSPayIn()
