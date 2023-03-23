# MACROPAD Hotkeys example: Universal Numpad

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                    # REQUIRED dict, must be named 'app'
    'name' : 'Navpad', # Application name
    'macros' : [           # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x100010, 'Home', [Keycode.HOME]),
        (0x101010, '^', [Keycode.UP_ARROW]),
        (0x100010, 'PgUp', [Keycode.PAGE_UP]),
        # 2nd row ----------
        (0x101010, '<', [Keycode.LEFT_ARROW]),
        (0x000000, '', []),
        (0x101010, '>', [Keycode.RIGHT_ARROW]),
        # 3rd row ----------
        (0x100010, 'End', [Keycode.END]),
        (0x101010, 'V', [Keycode.DOWN_ARROW]),
        (0x100010, 'PgDn', [Keycode.PAGE_DOWN]),
        # 4th row ----------
        (0x100800, 'Ins', [Keycode.INSERT]),
        (0x100000, 'Del', [Keycode.DELETE]),
        (0x100000, 'Back', [Keycode.BACKSPACE])
        # Encoder button ---
        # (0x000000, '', [Keycode.BACKSPACE])
    ]
}
