from AcyncAlchemy.AAMainClass import AAMainClass


class ModelsAAMainClass(AAMainClass):
    
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    connector = ModelsAAMainClass()
    print(f"logger file name: {connector.logger_name}")