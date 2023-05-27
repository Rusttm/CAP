# from CAPMain.CAPMainClass import CAPMainClass
from API_MS.MSLogger import MSLogger
class MSMainClass(MSLogger):
    logger_name = "msapi"

    def __init__(self):
        super().__init__()