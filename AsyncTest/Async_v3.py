# simple realize async in thread
# !!! works
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

async def greet_every_n_seconds(n: int):
    while True:
        print(f"My new Coroutine {n}sec")
        await asyncio.sleep(n)
    return True

async def loop_in_thread():
    task1 = asyncio.create_task(greet_every_two_seconds())
    task2 = asyncio.create_task(greet_every_three_seconds())
    await task1
    await task2


def main():
    new_loop = asyncio.new_event_loop()
    new_loop.run_until_complete(loop_in_thread())


if __name__ == '__main__':
    # main()

    import threading
    t = threading.Thread(target=main, args=())
    t.start()
    print("coroutines run")
