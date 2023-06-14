from AcyncSQL.ASQLLogger import ASQLLogger

class ASQLMainClass(ASQLLogger):
    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = ASQLMainClass()
    connect.logger.info("testing MainClass")
