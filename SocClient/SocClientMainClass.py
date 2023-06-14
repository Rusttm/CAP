# from https://gitlab.com/markelov-alex/hx-py-framework-evolution/-/blob/main/f_models/server_socket/v0/client.py


class SocClientMainClass(object):
    pass


"""
Simple socket client for testing servers.

https://docs.python.org/3/library/socket.html#example

Run one of the servers and a few of clients.

All servers are functionally identical, so the client is same for them all.
Only an implementation is different.

For more control, don't enable auto-reconnect, but restart the client on
each disconnection.
"""

import socket
import asyncio
import time

import asyncio


class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()
    on_con_lost = loop.create_future()
    message = 'Hello World!'
    transport, protocol = await loop.create_connection(lambda: EchoClientProtocol(message, on_con_lost), '127.0.0.1', 1978)
    # Wait until the protocol signals that the connection
    # is lost and close the transport.
    try:
        await on_con_lost
    finally:
        transport.close()


if __name__ == "__main__":
    # current_loop = asyncio.new_event_loop()
    # coro = main()
    # send_task = asyncio.run_coroutine_threadsafe(coro, current_loop)
    # send_task.result()
    asyncio.run(main())

    print("client run!")
