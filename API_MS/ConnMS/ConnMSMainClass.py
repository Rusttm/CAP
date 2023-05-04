from Main.CAPMainClass import CAPMainClass


class ConnMSMainClass(CAPMainClass):
    """ superclass for all MoiSklad connectors """
    id = 0

    def __init__(self):
        super().__init__()
        self.id += 1
        """ all connector have own id"""

    def get_conn_id(self):
        return self.id
