# simple realize async in thread

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
    async_tasks = []
    async_tasks.append(asyncio.create_task(greet_every_two_seconds()))
    async_tasks.append(asyncio.create_task(greet_every_three_seconds()))
    await asyncio.gather(*async_tasks)

def main():
    asyncio.run(loop_in_thread())

if __name__ == '__main__':
    # main()

    import threading
    t = threading.Thread(target=main, args=())
    t.start()
    print("asdfad")
