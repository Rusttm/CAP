import logging


class CAPMainClass(object):
    """ main logger file """
    logger = None
    def __init__(self, file_name="cap.log"):
        self.set_logger()

    def set_logger(self, name="main"):
        log_name = __name__
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)
        logger_handler = logging.FileHandler(f"{log_name}.log", mode="w")
        # logger_handler = logging.FileHandler("controller.log", mode="w")
        logger_formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s msg: %(message)s")
        logger_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_handler)
