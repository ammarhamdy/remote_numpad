from model.network import get_my_ip, validate_ip_address, get_connected_ssid
from view.mainView import MainView
from tkinter import Event
from values.string import app_name
from model.typewriter import Typewriter
from time import sleep
from threading import Thread
from model.udpHost import Host

MAIN_VIEW: MainView
host: Host
last_used_ip_address: str
pointer_x, pointer_y = 0, 0
pointer2_x, pointer2_y = 0, 0
window_x, window_y = 0, 0
is_minimized = False


def init_main_controller(main_view: MainView):
    global window_x, window_y, MAIN_VIEW, host, last_used_ip_address
    host = None
    last_used_ip_address = None
    MAIN_VIEW = main_view
    window_position = main_view.window.geometry().split("+")
    window_x = int(window_position[1])
    window_y = int(window_position[2])
    main_view.exit_button.config(command=exit_window)
    main_view.main_label.bind("<ButtonPress>", init_pointer_position)
    main_view.main_label.bind("<Motion>", drag_window)
    main_view.status_label.bind("<ButtonPress>", init_pointer2_position)
    main_view.status_label.bind("<Motion>", drag_window_by_pointer2)
    main_view.reconnect_button.bind("<ButtonPress>", reconnect)


def lunch():
    global last_used_ip_address
    ip_address = get_my_ip()
    last_used_ip_address = ip_address
    create_connection(ip_address)
    Thread(target=_lunch, args=(ip_address,), daemon=False).start()
    Thread(target=_show_connected_ssid, daemon=False).start()
    MAIN_VIEW.show()


def _lunch(ip_address):
    global MAIN_VIEW, host
    Typewriter(app_name).typing_sentence(MAIN_VIEW.main_label)
    sleep(Typewriter.get_required_typing_millis(app_name))
    MAIN_VIEW.add_widgets()
    show_connection_status(ip_address)
    MAIN_VIEW.main_label.bind("<Double-Button-1>", toggle_window_size)


def create_connection(ip_address):
    global host
    has_host = False
    try:
        host = Host(ip_address)
        has_host = True
    except Exception as error:
        print("cannot create host:", error)
    if has_host:
        try:
            host.start_receiving()
        except Exception as error:
            print("while trying to receive:", error)


def reconnect(_):
    Thread(target=_reconnect, daemon=False).start()


def _reconnect():
    global host, last_used_ip_address, MAIN_VIEW
    if host is None:
        return
    MAIN_VIEW.reconnect_button["state"] = "disabled"
    ip_address = get_my_ip()
    if ip_address == last_used_ip_address:
        MAIN_VIEW.reconnect_button["state"] = "normal"
        return
    # close current connection.
    host.close()
    # create new connection.
    last_used_ip_address = ip_address
    create_connection(ip_address)
    # show address
    show_connection_status(ip_address)
    _show_connected_ssid()
    # enable the button again
    sleep(.25)
    MAIN_VIEW.reconnect_button["state"] = "normal"


def _show_connected_ssid():
    global MAIN_VIEW
    ssid = get_connected_ssid()
    if ssid is None:
        MAIN_VIEW.bottom_label["text"] = ""
    else:
        MAIN_VIEW.bottom_label["text"] = ssid


def toggle_window_size(_):
    global is_minimized
    if is_minimized:
        MAIN_VIEW.maximize_window()
        is_minimized = False
    else:
        MAIN_VIEW.minimize_window()
        is_minimized = True


def show_connection_status(ip_address):
    global MAIN_VIEW
    if validate_ip_address(ip_address):
        MAIN_VIEW.show_connected(ip_address)
    else:
        MAIN_VIEW.show_no_connection_message()


def init_pointer_position(press_event):
    """  set x and y coordinates mouse position when it pressed the fame """
    global pointer_x, pointer_y
    if press_event.num == 1:
        pointer_x, pointer_y = press_event.x, press_event.y


def init_pointer2_position(press_event):
    """  set x and y coordinates mouse position when it pressed the fame """
    global pointer2_x, pointer2_y
    if press_event.num == 1:
        pointer2_x, pointer2_y = press_event.x, press_event.y


def drag_window(motion_event: Event):
    global pointer_x, pointer_y, window_x, window_y
    # when mouse is pressing on window frame.
    if motion_event.state == 272:  # 272 or 256
        x = window_x + (motion_event.x - pointer_x)
        y = window_y + (motion_event.y - pointer_y)
        MAIN_VIEW.window.geometry("+%d+%d" % (x, y))
        window_x, window_y = x, y


def drag_window_by_pointer2(motion_event: Event):
    global pointer2_x, pointer2_y, window_x, window_y
    # when mouse is pressing on window frame.
    if motion_event.state == 272:
        x = window_x + (motion_event.x - pointer2_x)
        y = window_y + (motion_event.y - pointer2_y)
        MAIN_VIEW.window.geometry("+%d+%d" % (x, y))
        window_x, window_y = x, y


def exit_window():
    global MAIN_VIEW, host
    if host is not None:
        host.close()
    MAIN_VIEW.exit()


if __name__ == "__main__":
    main_v = MainView()
    init_main_controller(main_v)
    lunch()
