from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSPayOut(ConnMSMainClass):
    """class to connect payments out"""

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ConnMSPayOut()
