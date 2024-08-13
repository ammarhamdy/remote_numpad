# window setting:
window_padding = 3  # px

# button_font_size
small_button_size = 30  # px
button_font_size = 15  # px

# typing delay time for type each character:
typing_delay_time = .15  # millis


# background frame
bg_frame_mini_width = 350  # px
bg_frame_mini_height = 100  # px
bg_frame_max_width = 450  # px
bg_frame_max_height = 200  # px
bg_frame_width = bg_frame_max_width
bg_frame_height = bg_frame_max_height

# window size
window_mini_width = bg_frame_mini_width + window_padding
window_mini_height = bg_frame_mini_height + window_padding
window_max_width = bg_frame_width + window_padding
window_max_height = bg_frame_height + window_padding
window_width = window_max_width
window_height = window_max_height


def minimize():
    global window_width, window_height, \
        bg_frame_width, bg_frame_height
    window_width = window_mini_width
    window_height = window_mini_height
    bg_frame_width = bg_frame_mini_width
    bg_frame_height = bg_frame_mini_height


def maximize():
    global window_width, window_height, \
        bg_frame_width, bg_frame_height
    window_width = window_max_width
    window_height = window_max_height
    bg_frame_width = bg_frame_max_width
    bg_frame_height = bg_frame_max_height
