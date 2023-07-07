from AcyncSQL.ASQLMainClass import ASQLMainClass

class GenASQLCreateBalTable(ASQLMainClass):
    """ create table and makes customers_inn col from requested data"""
    def __init__(self):
        super().__init__()

    async def request_inn_list(self):
        pass
