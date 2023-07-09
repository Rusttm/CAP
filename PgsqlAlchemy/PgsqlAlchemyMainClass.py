from PgsqlAlchemy.PgsqlAlchemyLogger import PgsqlAlchemyLogger

class PgsqlAlchemyMainClass(PgsqlAlchemyLogger):
    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = PgsqlAlchemyMainClass()
    connect.logger.info("testing MainClass")

