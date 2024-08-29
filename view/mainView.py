from tkinter import Tk, Button, Frame, Label
from values.color import *
from values import dimen
from values.dimen import minimize, maximize
from values.string import connection_failed_mess, cant_not_start, app_name


def get_background_layout(parent_layout):
    return Frame(
        parent_layout,
        background=BLACK
    )


def get_circle_text_button(parent_layout, foreground):
    return Button(
        parent_layout,
        borderwidth=0,
        highlightbackground=BLACK,
        highlightthickness=0,
        text="●",
        font=("", dimen.button_font_size),
        background=BLACK,
        foreground=foreground,
        activebackground=BLACK,
        activeforeground=WHITE
    )


def get_text_label(parent_layout):
    return Label(
        parent_layout,
        font=("", dimen.button_font_size * 2),
        background=BLACK,
        foreground=WHITE,
        wraplength=dimen.window_width - dimen.window_padding * 2
    )


def get_reconnect_button(parent_layout):
    return Button(
        parent_layout,
        borderwidth=0,
        highlightbackground=BLACK,
        highlightthickness=0,
        text="re",
        font=("", dimen.button_font_size),
        background=BLACK,
        foreground=WHITE,
        activebackground=BLACK,
        activeforeground=GRAY
    )


def get_status_label(parent_layout, text: str, anchor:str="center"):
    return Label(
        parent_layout,
        text=text,
        font=("", dimen.button_font_size),
        background=BLACK,
        foreground=WHITE,
        wraplength=dimen.window_width - dimen.window_padding,
        anchor=anchor
    )


class MainView:
    def __init__(self):
        self.is_alive = True
        self.window = Tk()
        self.config_window()
        # widgets:
        self.back_ground_layout = get_background_layout(self.window)
        self.main_label = get_text_label(self.window)
        self.exit_button = get_circle_text_button(self.window, RED)
        self.reconnect_button = get_reconnect_button(self.window)
        self.status_label = get_status_label(self.window, "")
        self.bottom_label = get_status_label(self.window, "", "w")
        self._add_widgets()

    def config_window(self):
        x = self.window.winfo_screenwidth() // 2 - dimen.window_width // 2
        y = self.window.winfo_screenheight() // 2 - dimen.window_height // 2
        self.window.geometry(f"{dimen.window_width}x{dimen.window_height}+{x}+{y}")
        self.window.config(background=WHITE)
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)

    def _add_widgets(self):
        self.back_ground_layout.place(
            x=dimen.window_padding,
            y=dimen.window_padding,
            width=dimen.window_width - dimen.window_padding * 2,
            height=dimen.window_height - dimen.window_padding * 2
        )
        self.main_label.place(
            x=dimen.window_padding,
            y=dimen.window_padding,
            width=dimen.window_width - dimen.window_padding * 2,
            height=dimen.window_height - dimen.window_padding * 2
        )

    def add_widgets(self):
        self.reconnect_button.place(
            x=dimen.window_padding,
            y=dimen.window_padding,
            width=dimen.small_button_size,
            height=dimen.small_button_size
        )
        self.exit_button.place(
            x=dimen.window_width - dimen.window_padding - dimen.small_button_size,
            y=dimen.window_padding,
            width=dimen.small_button_size,
            height=dimen.small_button_size
        )
        self.status_label.place(
            x=dimen.window_padding + dimen.small_button_size,
            y=dimen.window_padding,
            width=dimen.window_width - (dimen.small_button_size * 2 + dimen.window_padding * 2),
            height=dimen.small_button_size
        )
        self.bottom_label.place(
            x=dimen.window_padding,
            y=dimen.window_height - dimen.small_button_size - dimen.window_padding,
            width=dimen.window_width - dimen.window_padding * 2,
            height=dimen.small_button_size
        )

    def show(self):
        self.window.mainloop()

    def minimize_window(self):
        minimize()
        self.main_label.config(
            font=("", dimen.button_font_size),
            wraplength=dimen.window_width - dimen.window_padding)
        self._add_widgets()
        self.add_widgets()
        self.window.geometry(
            f"{dimen.window_width}x{dimen.window_height}")

    def maximize_window(self):
        maximize()
        self.main_label.config(
            font=("", dimen.button_font_size * 2),
            wraplength=dimen.window_width - dimen.window_padding
        )
        self._add_widgets()
        self.add_widgets()
        self.window.geometry(
            f"{dimen.window_width}x{dimen.window_height}"
        )

    def show_no_connection_message(self):
        if self.is_alive:
            self.window.config(background=RED)
            self.status_label["text"] = cant_not_start
            self.main_label["text"] = connection_failed_mess

    def show_connected(self, ip_address):
        self.main_label["text"] = ip_address
        self.status_label["text"] = app_name

    def exit(self):
        self.is_alive = False
        self.window.destroy()


if __name__ == "__main__":
    main_view = MainView()
    main_view._add_widgets()
    main_view.add_widgets()
    main_view.show()
