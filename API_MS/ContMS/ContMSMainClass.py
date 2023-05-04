from Main.CAPMainClass import CAPMainClass


class ContMSMainClass(CAPMainClass):
    """ superclass for all MoiSklad controllers """
    id = 0

    def __init__(self):
        super().__init__()
        self.id += 1
        """ all controllers have own id"""

    def get_cont_id(self):
        return self.id

