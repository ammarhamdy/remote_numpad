from threading import Thread
from time import sleep

from model import UDPServer
from model.network import get_my_ip, validate_ip_address
from view.mainView import MainView
from tkinter import Event
from values.string import title
from model.typewriter import Typewriter

MAIN_VIEW: MainView
pointer_x, pointer_y = 0, 0
pointer2_x, pointer2_y = 0, 0
window_x, window_y = 0, 0
HOST: UDPServer


def init_main_controller(main_view: MainView):
    global window_x, window_y, MAIN_VIEW, HOST
    MAIN_VIEW = main_view
    window_position = main_view.window.geometry().split("+")
    window_x = int(window_position[1])
    window_y = int(window_position[2])
    main_view.exit_button.config(command=exit_window)
    main_view.main_label.bind("<ButtonPress>", init_pointer_position)
    main_view.main_label.bind("<Motion>", drag_window)
    main_view.status_label.bind("<ButtonPress>", init_pointer2_position)
    main_view.status_label.bind("<Motion>", drag_window_by_pointer2)


def lunch():
    Thread(
        target=_lunch,
        daemon=True
    ).start()


def _lunch():
    ip_address = get_my_ip()
    Typewriter(title).start_typing(MAIN_VIEW.main_label)
    sleep(Typewriter.get_required_typing_millis(title) + 1)
    MAIN_VIEW.add_widgets()
    show_connection_status(ip_address)


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
    if motion_event.state == 272:
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
    global MAIN_VIEW
    MAIN_VIEW.exit()


if __name__ == "__main__":
    main_v = MainView()
    init_main_controller(main_v)
    lunch()
    main_v.show()

