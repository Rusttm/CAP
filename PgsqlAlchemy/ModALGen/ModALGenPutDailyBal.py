from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass
import datetime

class ModALGenPutDailyBal(ModALGenMainClass):
    def __init__(self):
        super().__init__()

    def get_data_for_update_daily_bal(self, table_year: datetime = None):
        pass


if __name__ == '__main__':
    generator = ModALGenPutDailyBal()
    print(generator.get_data_for_update_daily_bal(table_year=datetime.datetime.now().year))
