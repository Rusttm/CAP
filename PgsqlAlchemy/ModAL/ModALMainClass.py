from PgsqlAlchemy.PgsqlAlchemyMainClass import PgsqlAlchemyMainClass


class ModALMainClass(PgsqlAlchemyMainClass):
    
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ModALMainClass()
    print(f"logger file name: {connector.logger_name}")