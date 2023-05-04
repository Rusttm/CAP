from API_MS.ConnMS.ConnMSMainClass import ConnMSMainClass


class ConnMSPayOut(ConnMSMainClass):
    """class to connect payments out"""

    def say_hello(self):
        print("Hello World")

if __name__ == '__main__':
    connector = ConnMSPayOut()
    connector.say_hello()