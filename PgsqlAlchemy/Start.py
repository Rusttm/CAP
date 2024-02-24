from CAPMain.CAPMainClass import CAPMainClass
import asyncio

class Main(CAPMainClass):

    def __init__(self):
        super().__init__()

    def main(self):
        print("Update Service runs")




    async def main_async(self):
        await asyncio.sleep(2)
        print("You run asyncio update services")


if __name__ == '__main__':
    main_class = Main()
    loop = asyncio.new_event_loop()
    print(asyncio.run(main_class.main_async()))