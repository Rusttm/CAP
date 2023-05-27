import logging
from logging.handlers import RotatingFileHandler


class MSLogger(object):
    logger_name = "msapi"
    logger = None

    def __init__(self):
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.DEBUG)
        logger_handler = RotatingFileHandler(f"{self.logger_name}.log", mode="w", maxBytes=1*1024*1024)
        # logger_handler = logging.FileHandler("controller.log", mode="w")
        logger_formatter = logging.Formatter("%(asctime)s,%(msecs)d %(name)s %(levelname)s msg: %(message)s")
        logger_handler.setFormatter(logger_formatter)
        self.logger.addHandler(logger_handler)


if __name__ == '__main__':
    connector = MSLogger()
    connector.logger.info("resting")