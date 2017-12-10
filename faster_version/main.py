import pyHook, pythoncom
import pyautogui
import pyperclip
from pyHook import HookConstants, GetKeyState
import keyboard
import threading
import tkinter as tk

from faster_version.global_initializer import current_word, app, do_process_key, del_current_word

global suggestions
suggestions = ['suggestions' + str(i) for i in range(8)]


def OnKeyboardEvent(event):
    if not do_process_key:
        return True

    for i in range(8):
        if GetKeyState(HookConstants.VKeyToID('VK_CONTROL')) and HookConstants.IDToName(event.KeyID) == str(i):
            print("Ctrl " + str(i) + " pressed")

            global do_process_key
            do_process_key = False

            del_current_word(current_word)
            pyperclip.copy(suggestions[i])
            pyautogui.hotkey("ctrl", "v")

            do_process_key = True
            return True

    if True:
        print(event.Key)

    suggestions[0] = event.Key
    print()

    app.updateGui(suggestions)
    return True


# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
