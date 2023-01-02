# MACROPAD Hotkeys example: Microsoft Edge web browser for Windows

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                      # REQUIRED dict, must be named 'app'
    'name' : 'OBS', # Application name
    'macros' : [             # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, 'Face', [Keycode.WINDOWS, '2', -Keycode.WINDOWS, -Keycode.COMMAND, Keycode.CONTROL, '1']),
        (0x004000, 'Scr', [Keycode.WINDOWS, '2', -Keycode.WINDOWS, -Keycode.COMMAND, Keycode.CONTROL, '2']),
	(0x004000, 'Scr+Cam', [Keycode.WINDOWS, '2', -Keycode.WINDOWS, -Keycode.COMMAND, Keycode.CONTROL, '3']),
        # 2nd row ----------
        (0x004000, 'S+P', [Keycode.WINDOWS, '2', -Keycode.WINDOWS, -Keycode.COMMAND, Keycode.CONTROL, '4']),
        (0x004000, 'S+C+P', [Keycode.WINDOWS, '2', -Keycode.WINDOWS, -Keycode.COMMAND, Keycode.CONTROL, '5']),
	(0x004000, 'Pvt', [Keycode.WINDOWS, '2', -Keycode.WINDOWS, -Keycode.COMMAND, Keycode.CONTROL, '6']),
        # 3rd row ----------
        (0x000000, '?', []),
        (0x000000, '?', []),
        (0x000000, '?', []),
        # 4th row ----------
        (0x000000, '?', []),   # Adafruit in new window
        (0x000000, '?', []),   # Digi-Key in new window
        (0xFF0000, 'Mute', [ 0xAE]),
        # Encoder button ---
        (0x000000, '', [Keycode.CONTROL, 'w']) # Close tab
    ]
}
