from AcyncAlchemy.ModelsAA.ModelsAAMainClass import ModelsAAMainClass


class ModelsAACreator(ModelsAAMainClass):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ModelsAAMainClass()
    print(f"logger file name: {connector.logger_name}")