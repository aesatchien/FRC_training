import asyncio
import pickle
import datetime
import time

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, on_con_lost):
        self.message = message
        self.on_con_lost = on_con_lost

    def connection_made(self, transport):
        #transport.write(self.message.encode())
        transport.write(self.message)
        print('Data sent: {!r}'.format(pickle.loads(self.message)))

    def data_received(self, data):
        message = pickle.loads(data)
        print('Data received: {!r}'.format(message))

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.on_con_lost.set_result(True)


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.

    for i in range(5):
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()
        time.sleep(1.5)
        message = datetime.datetime.now()
        message = pickle.dumps(message)

        transport, protocol = await loop.create_connection(
            lambda: EchoClientProtocol(message, on_con_lost),
            '127.0.0.1', 1243)

        # Wait until the protocol signals that the connection
        # is lost and close the transport.
        try:
            await on_con_lost
        finally:
            transport.close()


asyncio.run(main())