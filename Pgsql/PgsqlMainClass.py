from Main.CAPMainClass import CAPMainClass

class PgsqlMainClass(CAPMainClass):
    logger_name = "Pgsql"
    def __init__(self):
        super().__init__()