import asyncio
from model.network import get_my_ip
import socket
from datetime import datetime


async def wait_for_data(address, port):
    # Get a reference to the current event loop because
    # we want to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    rsock, wsock = socket.socketpair()

    # Register the open socket to wait for data.
    reader, writer = await asyncio.open_connection(sock=rsock)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    while "18:15" not in str(datetime.today()):
        data = await reader.read(100)
        # Got data, we are done: close the socket
        print("Received:", data.decode())

    writer.close()
    await writer.wait_closed()

    # Close the second socket
    wsock.close()


async def tcp_echo_client(address, port):
    reader, writer = await asyncio.open_connection(address, port)

    print(f'Send: {1!r}')
    writer.write("1".encode())
    await writer.drain()

    data = await reader.read(1)
    print(f'Received: {data.decode()!r}')

    print('Close the connection')
    writer.close()
    await writer.wait_closed()


async def host(address, port):
    server = await asyncio.start_server(
        handle_echo,
        host=None,
        port=port,
        family=socket.SOCK_DGRAM,
        flags=socket.AI_PASSIVE,
        reuse_address=True,
        reuse_port=True
    )
    async with server:
        await server.serve_forever()


async def handle_echo(reader, writer):
    while "18:33" not in str(datetime.today()):
        data = await reader.read(1)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")

    print("Close the connection")
    writer.close()
    await writer.wait_closed()


if __name__ == "__main__":
    my_address = get_my_ip()
    print(f"My address:  {my_address}")
    # asyncio.run(wait_for_data(my_address, 1057))
    # asyncio.run(tcp_echo_client(my_address, 1057))
    asyncio.run(host(my_address, 1057))

