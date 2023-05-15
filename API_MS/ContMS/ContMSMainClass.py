from Main.CAPMainClass import CAPMainClass
# from API_MS.ConnMS.ConnMSConfig import ConnMSConfig
import configparser
import os
import pathlib


class ContMSMainClass(CAPMainClass):
    """ superclass for all MoiSklad controllers """
    id = 0

    def __init__(self):
        super().__init__()
        self.id += 1
        """ all controllers have own id"""
