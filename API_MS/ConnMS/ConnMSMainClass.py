class ConnMSMainClass(object):
    """ superclass for all MoiSklad connectors """
    id = 0

    def __init__(self):
        self.id += 1
        """ all connector have own id"""

    def get_conn_id(self):
        return self.id
