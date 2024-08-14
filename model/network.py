from _socket import socket, AF_INET, SOCK_DGRAM
from ipaddress import IPv4Address
import subprocess
import platform


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

def get_connected_ssid():
    os_name = platform.system()

    try:
        if os_name == "Windows":
            # Windows command
            result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
            result = result.decode("utf-8", errors="ignore").split("\n")
            for line in result:
                if "SSID" in line:
                    ssid = line.split(":")[1].strip()
                    return ssid

        elif os_name == "Linux":
            # Linux command
            result = subprocess.check_output(["nmcli", "-t", "-f", "active,ssid", "dev", "wifi"])
            result = result.decode("utf-8", errors="ignore").split("\n")
            for line in result:
                if line.startswith("yes:"):
                    ssid = line.split(":")[1]
                    return ssid

    except subprocess.CalledProcessError:
        return None

    return None



if __name__ == "__main__":
    my_address = get_my_ip()
    print(my_address)
    print(validate_ip_address(my_address))
    print(get_connected_ssid())
