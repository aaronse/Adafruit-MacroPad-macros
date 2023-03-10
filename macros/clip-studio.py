# MACROPAD Hotkeys example: Adobe Photoshop for Windows

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values



app = {                       # REQUIRED dict, must be named 'app'
    'name' : 'Clip Studio', # Application name
    'gamma' : True,
    'macros' : [              # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0xFF4040, 'Undo', [Keycode.CONTROL, 'z']),
        (0xFF2020, 'Redo', [Keycode.CONTROL, 'Z']),
        (0xFF1010, 'Brush', 'B'),   # Cycle brush modes
        # 2nd row ----------
        (0xFF1010, 'B&W', 'd'),     # Default colors
        (0xFF2020, 'Marquee', 'M'), # Cycle rect/ellipse marquee (select)
        (0xFF4040, 'Eraser', 'E'),  # Cycle eraser modes
        # 3rd row ----------
        (0xFF6000, 'Swap', 'x'),    # Swap foreground/background colors
        (0xB575DC, 'Move', 'v'),    # Move layer
        (0xFFA5B3, 'Fill', 'G'),    # Cycle fill/gradient modes
        # 4th row ----------
        (0xD8B2D1, 'Eyedrop', 'I'), # Cycle eyedropper/measure modes
        (0xFF8000, 'Wand', 'W'),    # Cycle "magic wand" (selection) modes
        (0xFBAED2, 'Heal', 'J'),    # Cycle "healing" modes
        # Encoder button ---
        (0x000000, '', [Keycode.CONTROL, Keycode.ALT, 'S']) # Save for web
    ]
}
