from _socket import socket, AF_INET, SOCK_DGRAM
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from pyautogui import press

keys = (
    None,
    "1", "2", "3",
    "4", "5", "6",
    "7", "8", "9",
    "0", ".", "esc",
    "prtsc", "tab", "=",
    None, None, None,
    None, None, "divide",
    "multiply", "backspace", "subtract",
    "add", "enter", None,
    None, None, None,
    "end", "down", "pgdn",
    "left", None, "right",
    "home", "up", "pgup",
    "insert", "delete", "{",
    "}", "[", "]"
)


def press_key(key_index):
    if key_index in range(0, len(keys)):
        if key_index is not None:
            press(keys[key_index])


class Server:
    executor = ThreadPoolExecutor(max_workers=2)
    port_number = 1057

    # time_out = 10

    def __init__(self, ip_address):
        self.is_receiving = True
        self.ip_address = ip_address
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ip_address, Server.port_number))
        # self.socket.settimeout(Server.time_out)

    # def shaking_hands(self):
    #     try:
    #         data, address = self.socket.recvfrom(1)
    #         print("Server receive:", data, "from:", address)
    #         if data == b'\x01':
    #             self.socket.sendto("2".encode(), address)
    #             data, address = self.socket.recvfrom(1)
    #             print("Server receive:", data, "from:", address)
    #             if data == b'\x03':
    #                 return True
    #     except Exception as ex:
    #         print("Exception:", ex)
    #         return False

    def start_receiving(self):
        Server.executor.submit(self._receiving)

    def _receiving(self):
        try:
            while self.is_receiving:
                data, address = self.socket.recvfrom(1)
                info = int.from_bytes(data, 'little')
                print(info, "from:", address)
                press_key(info)
        except Exception as ex:
            print("error while receiving!", ex)
            self.is_receiving = False

    def _send_ok(self):
        try:
            while self.is_receiving:
                print("Send \x01")
                self.socket.sendto(b'\x01', (self.ip_address, Server.port_number))
                sleep(1)
        except Exception as error:
            print(error)
            pass

    def send_ok(self):
        Server.executor.submit(self._send_ok)

    # def test(self):
    #     data, address = self.socket.recvfrom(1)
    #     print(data)
    #     data, address = self.socket.recvfrom(1)
    #     print(data)
    #     data, address = self.socket.recvfrom(1)
    #     print(data)

    def close(self):
        self.is_receiving = False
        # shutdown the server.
        self.socket.shutdown(0)
        self.socket.close()
        # shut down the worker (close thread).
        Server.executor.shutdown(wait=False)


if __name__ == "__main__":
    from network import get_my_ip

    my_address = get_my_ip()
    print("address:", my_address)
    server = Server(my_address)
    server.start_receiving()
    print("wait...")
    sleep(40)
    print("close")
    server.close()

    # status = server.shaking_hands()
    # print(status)
    # server.close()
    # server.test()
