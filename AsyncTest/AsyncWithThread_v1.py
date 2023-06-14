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
        print("My new Coroutine 3sec")
        await asyncio.sleep(3)
    return True


def loop_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task1 = loop.create_task(greet_every_two_seconds())
    loop.run_until_complete(task1)
    task2 = loop.create_task(greet_every_three_seconds())
    loop.run_until_complete(task2)
#

import threading
t = threading.Thread(target=loop_in_thread, args=())
t.start()
print("asdfad")
