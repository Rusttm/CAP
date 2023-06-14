# simple realize async in thread
# !!! doesnt works
import asyncio

## Define a coroutine that takes in a future

async def greet_every_two_seconds():
    while True:
        print("My new Coroutine 2sec")
        await asyncio.sleep(2)
    return True

async def greet_every_three_seconds():
    while True:
        print("My new Coroutine 4sec")
        await asyncio.sleep(4)
    return True


async def loop_in_thread():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(greet_every_two_seconds())
        tg.create_task(greet_every_three_seconds())

def main():
    asyncio.run(loop_in_thread())

if __name__ == '__main__':
    main()

    # import threading
    # t = threading.Thread(target=main, args=())
    # t.start()
    print("asdfad")
