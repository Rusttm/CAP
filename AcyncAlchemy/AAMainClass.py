from AcyncAlchemy.AALogger import AALogger

class AAMainClass(AALogger):
    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = AAMainClass()
    connect.logger.info("testing MainClass")
