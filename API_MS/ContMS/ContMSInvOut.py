from API_MS.ContMS.ContMSMainClass import ContMSMainClass
from API_MS.ConnMS.ConnMSInvOut import ConnMSInvOut
# import json


class ContMSInvOut(ContMSMainClass, ConnMSInvOut):
    """ controller class to get out invoices data"""

    def __init__(self):
        super().__init__()
        self.logger.debug(f"module {__class__.__name__} started")


if __name__ == '__main__':
    controller = ContMSInvOut()
    # data = controller.get_invout_filtered_by_date(from_date="2023-01-01", to_date="2023-02-01", to_file=True)
    data = controller.get_invout_filtered_by_date(from_date="2022-12-01", to_date="2022-12-03", to_file=True)
