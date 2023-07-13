from PgsqlAlchemy.ModALGen.ModALGenMainClass import ModALGenMainClass
import datetime

class ModALGenPutDailyProfit(ModALGenMainClass):
    def __init__(self):
        super().__init__()

    def get_data_for_update_daily_profit(self, table_year: datetime = None):
        pass


if __name__ == '__main__':
    generator = ModALGenPutDailyProfit()
    print(generator.get_data_for_update_daily_profit(table_year=datetime.datetime.now().year))
