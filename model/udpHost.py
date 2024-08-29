from _socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
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
    "}", "(", ")"
)


def press_key(key_index):
    if -1 > key_index > len(keys):
        return
    value = keys[key_index]
    if value is None:
        return
    print(f">>{value}")
    press(value)


class Host:
    port_number = 1057
    close_code = 90

    def __init__(self, ip_address):
        self.is_receiving = False
        self.ip_address = ip_address
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ip_address, Host.port_number))

    def start_receiving(self):
        self.is_receiving = True
        Thread(target=self._receiving, daemon=False).start()

    def _receiving(self):
        try:
            while self.is_receiving:
                data, _ = self.socket.recvfrom(1)
                self.handle(data)
        except Exception as error:
            print("error while receiving!", error)

    def handle(self, data):
        if data is None:
            return
        info: int = int.from_bytes(data, 'little')
        if info == Host.close_code:
            self._close()
        else:
            press_key(info)

    def close(self):
        try:
            self.socket.sendto(
                int.to_bytes(Host.close_code),
                (self.ip_address, Host.port_number)
            )
        except Exception as error:
            print("host while sending close code", error)

    def _close(self):
        self.is_receiving = False
        # shutdown the server.
        self.socket.close()


if __name__ == "__main__":
    from network import get_my_ip

    my_address = get_my_ip()
    print("address:", my_address)
    server = Host(my_address)
    server.start_receiving()
