from PgsqlAlchemy.PgsqlAlchemyMainClass import PgsqlAlchemyMainClass


class ModALUpdaterMainClass(PgsqlAlchemyMainClass):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ModALUpdaterMainClass()
    print(f"logger file name: {connector.logger_name}")
    connector.logger.info("testing ModALFillerMainClass")
