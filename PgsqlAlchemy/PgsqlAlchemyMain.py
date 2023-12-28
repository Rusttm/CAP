from PgsqlAlchemy.PgsqlAlchemyMainClass import PgsqlAlchemyMainClass


class PgsqlAlchemyTablesUpdater(PgsqlAlchemyMainClass):
    def __init__(self):
        super().__init__()

    def update_tables_from_ms(self):
        from PgsqlAlchemy.ModALUpdaters.ModALUpdCustBal import ModALUpdCustBal
        cust_bal_updater = ModALUpdCustBal()
        cust_bal_updater.update_cust_bal()



if __name__ == "__main__":
    connect = PgsqlAlchemyTablesUpdater()
    connect.logger.info("testing PgsqlAlchemyTablesUpdater")