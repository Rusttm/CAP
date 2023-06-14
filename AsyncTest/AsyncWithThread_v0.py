# simple realize async in thread

import threading
import asyncio

async def greet_every_two_seconds():
    while True:
        print("My new Coroutine")
        await asyncio.sleep(2)

def loop_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = loop.create_task(greet_every_two_seconds())
    loop.run_until_complete(task)


t = threading.Thread(target=loop_in_thread, args=())
t.start()
print("asdfad")