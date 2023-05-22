from SQLAlchem.SQLAlchemLogger import SQLAlchemLogger

class SQLAlchemMainClass(SQLAlchemLogger):
    def __init__(self):
        # print("test class")
        super().__init__()


if __name__ == "__main__":
    connect = SQLAlchemMainClass()
    connect.logger.info("testing MainClass")

