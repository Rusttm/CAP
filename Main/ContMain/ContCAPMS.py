from Main.ContMain.ContCAPMainClass import ContCAPMainClass
from API_MS.ContMS.ContMSBalance import ContMSBalance

class ContCAPMS(ContCAPMainClass):
    """ MoiSklad API controller"""

    def __init__(self, *args):
        super().__init__()
        self.id = ContCAPMS.id = super().get_cont_id()
        print(self.id)

    def get_balance(self):
        controller = ContMSBalance()
        return None


if __name__ == '__main__':
    controller1 = ContCAPMS()
    controller1.get_balance()


