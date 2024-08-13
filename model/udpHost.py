from _socket import socket, AF_INET, SOCK_DGRAM
from concurrent.futures import ThreadPoolExecutor
from pynput.keyboard import Key, Controller, KeyCode

keyboard = Controller()

keys = (
    None,
    KeyCode.from_char(char="1"),
    KeyCode.from_char(char="2"),
    KeyCode.from_char(char="3"),
    KeyCode.from_char(char="4"),
    KeyCode.from_char(char="5"),
    KeyCode.from_char(char="6"),
    KeyCode.from_char(char="7"),
    KeyCode.from_char(char="8"),
    KeyCode.from_char(char="9"),
    KeyCode.from_char(char="0"),
    KeyCode.from_char(char="."),
    Key.esc,
    Key.print_screen,
    Key.tab,
    KeyCode.from_char(char="="),
    None, None, None, None, None,
    KeyCode.from_char(char="/"),
    KeyCode.from_char(char="*"),
    Key.backspace,
    KeyCode.from_char(char="-"),
    KeyCode.from_char(char="+"),
    Key.enter,
    None, None, None, None,
    Key.end,
    Key.down,
    Key.page_down,
    Key.left,
    None,
    Key.right,
    Key.home,
    Key.up,
    Key.page_up,
    Key.insert,
    Key.delete,
    KeyCode.from_char(char="{"),
    KeyCode.from_char(char="}"),
    KeyCode.from_char(char="["),
    KeyCode.from_char(char="]"),
)


def press_key(key_index):
    if -1 > key_index > len(keys):
        return
    value = keys[key_index]
    if value is None:
        return
    keyboard.tap(value)


class Host:
    executor = ThreadPoolExecutor(max_workers=1)
    port_number = 1057
    close_code = 90

    def __init__(self, ip_address):
        self.is_receiving = False
        self.ip_address = ip_address
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((ip_address, Host.port_number))

    def start_receiving(self):
        self.is_receiving = True
        Host.executor.submit(self._receiving)

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
        # shut down the worker (close thread).
        Host.executor.shutdown(wait=False)


if __name__ == "__main__":
    from network import get_my_ip

    my_address = get_my_ip()
    print("address:", my_address)
    server = Host(my_address)
    server.start_receiving()
