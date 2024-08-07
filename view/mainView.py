from tkinter import Tk, Button, Frame, Label
from values.color import *
from values.dimen import *
from values.string import title


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
        font=("", button_font_size),
        background=BLACK,
        foreground=foreground,
        activebackground=BLACK,
        activeforeground=WHITE
    )

def get_text_label(parent_layout):
    return Label(
        parent_layout,
        font=("", button_font_size * 2),
        background=BLACK,
        foreground=WHITE,
        wraplength=window_width - window_padding * 2
    )


def get_reconnect_button(parent_layout):
    return Button(
        parent_layout,
        borderwidth=0,
        highlightbackground=BLACK,
        highlightthickness=0,
        text="re",
        font=("", button_font_size),
        background=BLACK,
        foreground=WHITE,
        activebackground=BLACK,
        activeforeground=GRAY,
        state="disabled"
    )


def get_status_label(parent_layout, text: str):
    return Label(
        parent_layout,
        text=text,
        font=("", button_font_size),
        background=BLACK,
        foreground=WHITE,
        wraplength=window_width - window_padding,
        anchor="center"
    )


class MainView:
    def __init__(self):
        self.is_alive = True
        self.window = Tk()
        self.config_window()
        self.init_widgets()
        self._add_widgets()

    def config_window(self):
        x = self.window.winfo_screenwidth()//2 - window_width//2
        y = self.window.winfo_screenheight()//2 - window_height//2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.config(background=WHITE)
        self.window.overrideredirect(True)

    def init_widgets(self):
        self.back_ground_layout = get_background_layout(self.window)
        self.main_label = get_text_label(self.window)
        self.exit_button = get_circle_text_button(self.window, RED)
        self.reconnect_button = get_reconnect_button(self.window)
        self.status_label = get_status_label(self.window, "")

    def _add_widgets(self):
        self.back_ground_layout.place(
            x=window_padding,
            y=window_padding,
            width=window_width - window_padding*2,
            height=window_height - window_padding*2
        )
        self.main_label.place(
            x=window_padding,
            y=window_padding,
            width=window_width - window_padding * 2,
            height=window_height - window_padding * 2
        )

    def add_widgets(self):
        self.reconnect_button.place(
            x=window_padding,
            y=window_padding,
            width=small_button_size,
            height=small_button_size
        )
        self.exit_button.place(
            x=window_width - window_padding - small_button_size,
            y=window_padding,
            width=small_button_size,
            height=small_button_size
        )
        self.status_label.place(
            x=window_padding + small_button_size,
            y=window_padding,
            width=window_width - (small_button_size * 2 + window_padding * 2),
            height=small_button_size
        )


    def show(self):
        self.window.mainloop()

    def show_connected_and_receiving(self):
        self.window.config(background=GREEN)
        self.status_label["text"] = "connected with client"
        self.main_label["text"] = "receiving..."
        self.reconnect_button["state"] = "disabled"

    def show_no_connection_message(self):
        if self.is_alive:
            self.window.config(background=RED)
            self.status_label["text"] = "can not start"
            self.reconnect_button["state"] = "normal"
            self.main_label["text"] = "Please connect with your mobil hot spot"

    def show_connected(self, ip_address):
        self.main_label["text"] = ip_address
        self.status_label["text"] = "My ip address"

    def exit(self):
        self.is_alive = False
        self.window.destroy()


if __name__ == "__main__":
    main_view = MainView()
    main_view.show()

