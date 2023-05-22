from CAPMain.CAPMainClass import CAPMainClass

class ContCAPMainClass(CAPMainClass):
    """ programm controllers super class"""
    id = 0

    def __init__(self):
        super().__init__()
        self.id += 1
        """ all controllers have own id"""

    def get_cont_id(self):
        return self.id
