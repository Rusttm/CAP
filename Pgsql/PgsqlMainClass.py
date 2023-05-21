from Main.CAPMainClass import CAPMainClass
from Pgsql.PgsqlLogger import PgsqlLogger


class PgsqlMainClass(PgsqlLogger, CAPMainClass):

    def __init__(self):
        super().__init__()