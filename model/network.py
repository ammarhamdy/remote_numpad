from _socket import socket, AF_INET, SOCK_DGRAM
from ipaddress import IPv4Address


def validate_ip_address(address: str):
    try:
        ipv4_address = IPv4Address(address)
        return not ipv4_address.is_loopback and ipv4_address.is_private
    except Exception as ex:
        print(ex)
        return False


def get_my_ip():
    soc = socket(AF_INET, SOCK_DGRAM)
    soc.settimeout(0)
    try:
        # doesn't even have to be reachable
        soc.connect(('10.254.254.254', 1))
        ip_address = soc.getsockname()[0]
    except Exception as ex:
        print(ex)
        ip_address = '127.0.0.1'
    finally:
        soc.close()
    return ip_address


if __name__ == "__main__":
    my_address = get_my_ip()
    print(my_address)
    print(validate_ip_address(my_address))
