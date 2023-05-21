from SocSrv.SocSrvLogger import SocSrvLogger


class SocketMainClass(SocSrvLogger):
    logger_name = "SocketService"

    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = SocketMainClass()
    connect.logger.info("testing")

