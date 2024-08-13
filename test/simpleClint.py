from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from time import sleep


class Client:
    def __init__(self, ip, port=5056):
        self.ip_address = ip
        self.socket_client = socket(family=AF_INET, type=SOCK_DGRAM)
        try:
            # if the server not open this line make error.
            self.socket_client.connect((ip, port))
        except Exception as error:
            print(f"make sure that the server is running: {error}")
        self.socket_client.settimeout(2)

    def close(self):
        self.socket_client.close()

    def start(self):
        number = 1
        self.socket_client.send(number.to_bytes(1))
        print("SEND:", number)
        number = 3
        self.socket_client.send(number.to_bytes(1))
        print("SEND:", number)


if __name__ == '__main__':
    # print(gethostbyname(gethostname()))
    clint = Client(ip="192.168.1.18")
    clint.start()
    clint.close()
