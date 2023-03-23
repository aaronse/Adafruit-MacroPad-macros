"""
A fairly straightforward macro/hotkey program for Adafruit MACROPAD.
Macro key setups are stored in the /macros folder (configurable below),
load up just the ones you're likely to use. Plug into computer's USB port,
use dial to select an application macro set, press MACROPAD keys to send
key sequences.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import displayio
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode

# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'


# Based on Adafruit 8 bit gamma lookup map:
# - https://learn.adafruit.com/led-tricks-gamma-correction/the-longer-fix
# - https://learn.adafruit.com/image-correction-for-rgb-led-matrices/still-images-using-python
gamma8 = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255]


def adjustGamma(color):
    r = color >> 16 & 255
    g = color >> 8 & 255
    b = color & 255

   # Gamma correction, adjust light levels to factor in non linear response of our eyes.
    r = gamma8[r]
    g = gamma8[g]
    b = gamma8[b]

    return (r << 16) + (g << 8) + b


# CLASSES AND FUNCTIONS ----------------

class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']
        self.gamma = appdata.get('gamma', False)

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
        group[13].text = self.name   # Application name
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                if self.gamma:
                    macropad.pixels[i] = adjustGamma(self.macros[i][0])
                else:
                    macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                macropad.pixels[i] = 0
                group[i].text = ''
        macropad.keyboard.release_all()
        macropad.pixels.show()
        macropad.display.refresh()


# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False

# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
group.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, -2),
                         anchor_point=(0.5, 0.0)))
macropad.display.show(group)

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            pass

if not apps:
    group[13].text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True:
        pass

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()
last_sequence = []
isEncoderScrollMode  = False

# MAIN LOOP ----------------------------

while True:
    # Read encoder position. If it's changed, switch apps.
    position = macropad.encoder

    # If treating encoder as scroller, then map encoder rotation to Up/Down arrow movement(s)
    scrollDelta = 0 if last_position is None else last_position - position

    if position != last_position:
        if isEncoderScrollMode:
            scrollDelta = min(5, max(-5, last_position - position))
        else:
            app_index = position % len(apps)
            apps[app_index].switch()
            
    last_position = position

    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:

        # No 13th macro explicitly defined, so transition encoder to Up/Down 'Scroll mode'
        if len(apps[app_index].macros) < 13 and last_encoder_switch != encoder_switch:
            isEncoderScrollMode = not isEncoderScrollMode
            if (isEncoderScrollMode):
                group[13].text = 'Scroll Mode'
                macropad.display.refresh()
            else:
                apps[app_index].switch()

            continue

        last_encoder_switch = encoder_switch

        key_number = 12 # else process below as 13th macro
        pressed = encoder_switch
    elif isEncoderScrollMode:
        key_number = 1
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.

    if isEncoderScrollMode:
        if scrollDelta > 0:
            sequence = [Keycode.UP_ARROW, -Keycode.UP_ARROW] * 3 * scrollDelta
            pressed = True
        elif scrollDelta < 0:
            sequence = [Keycode.DOWN_ARROW, -Keycode.DOWN_ARROW] * 3 * abs(scrollDelta)
            pressed = True
        else:
            sequence = last_sequence
            pressed = False
    else:
        sequence = apps[app_index].macros[key_number][2]

    if pressed:
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = 0x000000
            macropad.pixels.show()
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.press(item)
                else:
                    macropad.keyboard.release(-item)
            else:
                macropad.keyboard_layout.write(item)
    else:
        # Release any still-pressed modifier keys
        for item in sequence:
            if isinstance(item, int) and item >= 0:
                macropad.keyboard.release(item)
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()

    last_sequence = sequence
