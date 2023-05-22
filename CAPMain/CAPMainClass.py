from CAPMain.CAPLogger import CAPLogger


class CAPMainClass(CAPLogger):
    """ main logger file """
    # 
    # logger = None
    # """ main class logger in CAP project"""

    def __init__(self, file_name="cap.log"):
        super().__init__()
    #     self.set_logger("CAPMainClass")
    # 
    # def set_logger(self, logger_name="main"):
    #     self.logger = logging.getLogger(logger_name)
    #     self.logger.setLevel(logging.DEBUG)
    #     logger_handler = logging.FileHandler(f"{logger_name}.log", mode="w")
    #     # logger_handler = logging.FileHandler("controller.log", mode="w")
    #     logger_formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s msg: %(message)s")
    #     logger_handler.setFormatter(logger_formatter)
    #     self.logger.addHandler(logger_handler)
    # 
    # def get_logger(self):
    #     return self.logger
